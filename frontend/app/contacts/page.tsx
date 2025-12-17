// frontend/app/contacts/page.tsx

export default async function Contacts() {
  const res = await fetch("http://localhost:8000/contacts", { cache: "no-store" })
  const contacts = await res.json()

  return (
    <div className="p-8">
      <h1>Contacts</h1>
      {contacts.map((c:any) => (
        <div key={c.id} className="border p-2 my-2">
          <b>{c.name}</b> — {c.email}<br/>
          {c.affiliation} | {c.field}
        </div>
      ))}
    </div>
  )
}
