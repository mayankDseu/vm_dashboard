import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

const Dashboard = () => {
    const [results, setResults] = useState({});
    const [loading, setLoading] = useState(false);

    const fetchResults = async () => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/get-results`);
            setResults(res.data);
        } catch (error) {
            console.error("Error fetching results:", error);
        }
        setLoading(false);
    };

    useEffect(() => {
        fetchResults();
    }, []);

    const getStatusColor = (status) => {
        if (status === "OK") return "green";
        if (status === "MISSING_HEAD" || status === "DEFECT") return "red";
        return "orange";
    };

    return (
        <div className="dashboard">
            <div className="header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px" }}>
                <h1>🎥 VMS Dashboard</h1>
                <button className="refresh-btn" onClick={fetchResults} disabled={loading}>
                    🔄 Refresh
                </button>
            </div>

            <div className="summary-section" style={{ paddingLeft: "20px" }}>
                <p>🟢 Active Streams: <b>{Object.keys(results).length}</b></p>
            </div>


            <div className="streams-grid">
                {Object.entries(results).map(([streamId, frames]) => {
                    const totalDetections = frames.flatMap(f => f.results).length;
                    const totalDefects = frames.flatMap(f => f.results)
                        .filter(r => r.classification.class !== "OK").length;

                    const alerts = frames.flatMap(f =>
                        f.results.map(r => ({
                            frame: f.frame,
                            ...r
                        }))
                    ).filter(r => r.classification.class !== "OK");

                    const latestFrame = frames.at(-1)?.frame || 0;

                    return (
                        <div
                            key={streamId}
                            className="stream-card"
                            style={{
                                border: `2px solid ${totalDefects > 0 ? "red" : totalDetections > 0 ? "green" : "orange"}`
                            }}
                        >
                            <h2>📺 Stream {streamId}</h2>

                            <img
                                src={`${API_BASE}/static/stream_${streamId}/frame_${latestFrame}.jpg`}
                                alt="Latest frame"
                                className="stream-image"
                            />

                            <p>📦 Total Frames Processed: {frames.length}</p>
                            <p>🧠 Total Detections: {totalDetections}</p>
                            <p>🚨 Alerts (Defects): <b style={{ color: totalDefects > 0 ? "red" : "green" }}>{totalDefects}</b></p>

                            {alerts.length > 0 && (
                                <div className="alerts-box">
                                    <h3>⚠️ Alerts</h3>
                                    {alerts.map((r, i) => (
                                        <div key={i} className="alert-row">
                                            ❗ <b style={{ color: getStatusColor(r.classification.class) }}>
                                                {r.classification.class}
                                            </b> detected in <b>{r.detection.label}</b> on frame <b>{r.frame}</b> (
                                            {r.classification.confidence})
                                        </div>

                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Dashboard;
