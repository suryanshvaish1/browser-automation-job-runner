"use client"

import { useEffect, useState } from "react"

export default function LogViewer({ jobId }: any) {

  const [logs, setLogs] = useState<any[]>([])

  useEffect(() => {

    if (!jobId) return

    const socket = new WebSocket(
      `ws://localhost:8000/ws/${jobId}`
    )

    socket.onmessage = (event) => {

      const data = JSON.parse(event.data)

      setLogs((prev) => [...prev, data])
    }

    return () => socket.close()

  }, [jobId])

  return (
    <div>

      <h2>Logs</h2>

      {
        logs.map((log, index) => (
          <div key={index}>
            {log.event} - {log.message}
          </div>
        ))
      }

    </div>
  )
}