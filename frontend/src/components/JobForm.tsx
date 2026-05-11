"use client"

import { useState } from "react"
import axios from "axios"

export default function JobForm({ setJobId }: any) {

  const [url, setUrl] = useState("")
  const [goal, setGoal] = useState("")

  const submitJob = async () => {

    const response = await axios.post(
      "http://localhost:8000/jobs",
      {
        url,
        goal
      }
    )

    setJobId(response.data.job_id)
  }

  return (
    <div style={{ marginBottom: "20px" }}>

      <input
        style={{
          padding: "10px",
          width: "400px",
          border: "1px solid white",
          color: "white",
          background: "black"
        }}
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <br /><br />

      <input
        style={{
          padding: "10px",
          width: "400px",
          border: "1px solid white",
          color: "white",
          background: "black"
        }}
        placeholder="Enter Goal"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      />

      <br /><br />

      <button
        style={{
          padding: "10px 20px",
          cursor: "pointer"
        }}
        onClick={submitJob}
      >
        Submit Job
      </button>

    </div>
  )
}