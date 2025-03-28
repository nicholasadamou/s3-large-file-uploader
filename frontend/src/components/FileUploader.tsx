import React, { useState } from "react";
import axios from "axios";

const CHUNK_SIZE = 10 * 1024 * 1024; // 10MB
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:4000/api";

export default function FileUploader() {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) {
      setStatus("No file selected");
      return;
    }

    try {
      setIsUploading(true);
      setStatus("Starting upload...");
      setProgress(0);

      const file = e.target.files[0];
      const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
      const userId = "demo-user";

      // Step 1: Start Upload
      const { data: startRes } = await axios.post(`${API_BASE_URL}/start-upload`, {
        filename: file.name,
        contentType: file.type,
        userId,
      });
      const { uploadId, key } = startRes;

      // Step 2: Upload Each Chunk using Signed URLs
      for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_SIZE;
        const end = Math.min(start + CHUNK_SIZE, file.size);
        const chunk = file.slice(start, end);
        const partNumber = i + 1;

        // Get signed URL from backend
        const {
          data: { signedUrl },
        } = await axios.get(`${API_BASE_URL}/get-signed-url`, {
          params: { uploadId, key, partNumber },
        });

        // Upload directly to S3
        const uploadRes = await fetch(signedUrl, {
          method: "PUT",
          body: chunk,
        });

        if (!uploadRes.ok) {
          throw new Error(`Failed to upload part ${partNumber}: ${uploadRes.statusText}`);
        }

        const ETag = uploadRes.headers.get("ETag")?.replace(/"/g, "");

        // Notify backend
        await axios.post(`${API_BASE_URL}/upload-part`, {
          uploadId,
          key,
          partNumber,
          ETag,
          userId,
        });

        setProgress(Math.round(((i + 1) / totalChunks) * 100));
      }

      // Step 3: Complete Upload
      const { data: completeRes } = await axios.post(`${API_BASE_URL}/complete-upload`, {
        uploadId,
        key,
        userId,
      });

      setStatus(`✅ Upload complete! File URL: ${completeRes.location}`);
    } catch (error) {
      console.error("Upload failed:", error);
      setStatus(`❌ Upload failed: ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Large File Uploader (Signed URL)</h2>
      <input type="file" onChange={handleUpload} disabled={isUploading} />
      <div style={{ marginTop: "10px" }}>
        {isUploading && (
          <div>
            <progress value={progress} max="100" style={{ width: "100%" }} />
            <p>Progress: {progress}%</p>
          </div>
        )}
        {status && <p>{status}</p>}
      </div>
    </div>
  );
}
