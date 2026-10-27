from app.models.document_event import DocumentEvent


def test_revisor_no_puede_eliminar(client, as_role, make_doc):
    doc_id = make_doc("recibido")
    as_role("revisor_documental")
    assert client.delete(f"/documents/{doc_id}").status_code == 403


def test_transicion_invalida_400(client, as_role, make_doc):
    doc_id = make_doc("recibido")
    as_role("revisor_documental")
    r = client.post(
        f"/documents/{doc_id}/review", json={"new_status": "revisado"}
    )
    assert r.status_code == 400


def test_usuario_no_ve_events(client, as_role, make_doc):
    doc_id = make_doc("recibido")
    as_role("usuario_documental")
    assert client.get(f"/documents/{doc_id}/events").status_code == 403


def test_decision_deja_evento(client, as_role, make_doc, db):
    doc_id = make_doc("revisado")
    as_role("admin_documental")
    r = client.post(
        f"/documents/{doc_id}/decide", json={"new_status": "aprobado"}
    )
    assert r.status_code == 200
    s = db()
    ev = s.query(DocumentEvent).filter_by(document_id=doc_id).one()
    assert (ev.previous_status, ev.new_status) == ("revisado", "aprobado")
    s.close()