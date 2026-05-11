"use client"

import { useState } from "react"

import JobForm from "../src/components/JobForm"
import LogViewer from "../src/components/LogViewer"

export default function Home() {

  const [jobId, setJobId] = useState("")

  return (
    <main style={{ padding: "20px" }}>

      <h1>Kustodian Browser Automation</h1>

      <JobForm setJobId={setJobId} />

      <LogViewer jobId={jobId} />

    </main>
  )
}