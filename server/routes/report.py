from flask import Blueprint, Response, jsonify, current_app, request 
from sqlalchemy import text
import csv
import io

report_bp = Blueprint("report", __name__)

@report_bp.route("/report/volunteer-history/csv", methods=["GET"])
def export_volunteer_history_csv():
    admin_user_id = request.args.get("admin_user_id")

    if not admin_user_id:
        return {"error": "admin_user_id required"}, 400

    engine = current_app.config["ENGINE"]

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT 
                u.name AS volunteer_name,
                e.name AS event_name,
                e.date AS date,
                e.location AS location,
                e.description AS description
            FROM matches m
            JOIN events e ON m.event_id = e.id
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN users u ON v.user_id = u.id
            WHERE e.ownerid = :admin_user_id
                AND m.status = 'confirmed'
            ORDER BY e.date DESC
        """), {"admin_user_id": admin_user_id}).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Volunteer Name", "Event Name", "Date", "Location", "Description"])

    for row in rows:
        writer.writerow(list(row))

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=volunteer_report.csv"}
    )
