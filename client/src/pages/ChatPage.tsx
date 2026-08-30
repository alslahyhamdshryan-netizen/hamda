import { useMemo, useState } from "react";
import {
  CheckCheck,
  Image,
  Mic,
  MoreVertical,
  Paperclip,
  Phone,
  Search,
  Send,
  Smile,
  Video,
} from "lucide-react";

type Message = {
  id: number;
  text: string;
  time: string;
  mine?: boolean;
  read?: boolean;
};

type Conversation = {
  id: number;
  name: string;
  role: string;
  initials: string;
  color: string;
  preview: string;
  time: string;
  unread?: number;
  online?: boolean;
  messages: Message[];
};

const initialConversations: Conversation[] = [
  {
    id: 1,
    name: "سارة عبدالله",
    role: "أخصائية موارد بشرية",
    initials: "س",
    color: "#2e719c",
    preview: "سأرسل لك التقرير خلال قليل.",
    time: "10:42 ص",
    unread: 2,
    online: true,
    messages: [
      { id: 1, text: "صباح الخير، هل اطلعت على تحديثات ملف التأمين؟", time: "10:34 ص" },
      { id: 2, text: "صباح النور سارة، نعم اطلعت عليها. كل شيء واضح.", time: "10:37 ص", mine: true, read: true },
      { id: 3, text: "ممتاز. سأرسل لك التقرير النهائي خلال قليل.", time: "10:42 ص" },
    ],
  },
  {
    id: 2,
    name: "أحمد محمد العريقي",
    role: "مدير تقنية المعلومات",
    initials: "أ",
    color: "#5367a4",
    preview: "تم تحديث صلاحيات النظام.",
    time: "أمس",
    online: true,
    messages: [
      { id: 1, text: "تم تحديث صلاحيات النظام للفريق.", time: "أمس 04:20 م" },
      { id: 2, text: "شكرًا أحمد، سأراجعها اليوم.", time: "أمس 04:25 م", mine: true, read: true },
    ],
  },
  {
    id: 3,
    name: "خالد علي",
    role: "محاسب أول",
    initials: "خ",
    color: "#9a6746",
    preview: "هل يمكن اعتماد الطلب؟",
    time: "الأحد",
    messages: [{ id: 1, text: "هل يمكن اعتماد طلب الإجازة؟", time: "الأحد 01:15 م" }],
  },
  {
    id: 4,
    name: "فريق الموارد البشرية",
    role: "مجموعة · 6 أعضاء",
    initials: "م",
    color: "#267b70",
    preview: "نورة: موعد الاجتماع غدًا.",
    time: "السبت",
    messages: [{ id: 1, text: "نورة: موعد الاجتماع غدًا الساعة 9 صباحًا.", time: "السبت 11:00 ص" }],
  },
];

export default function ChatPage() {
  const [conversations, setConversations] = useState(initialConversations);
  const [selectedId, setSelectedId] = useState(1);
  const [query, setQuery] = useState("");
  const [draft, setDraft] = useState("");
  const selected = conversations.find((conversation) => conversation.id === selectedId) ?? conversations[0];
  const filtered = useMemo(
    () => conversations.filter((conversation) => `${conversation.name} ${conversation.role}`.includes(query)),
    [conversations, query],
  );

  const selectConversation = (id: number) => {
    setSelectedId(id);
    setConversations((current) => current.map((conversation) => conversation.id === id ? { ...conversation, unread: 0 } : conversation));
  };

  const sendMessage = () => {
    const text = draft.trim();
    if (!text) return;
    setConversations((current) => current.map((conversation) => conversation.id === selected.id
      ? { ...conversation, preview: text, time: "الآن", messages: [...conversation.messages, { id: Date.now(), text, time: "الآن", mine: true, read: true }] }
      : conversation));
    setDraft("");
  };

  return (
    <div className="chat-page" dir="rtl">
      <section className="chat-contacts panel">
        <div className="chat-contacts-head">
          <div><h2>المحادثات</h2><span>{conversations.length} محادثات نشطة</span></div>
          <button className="icon-button" aria-label="خيارات المحادثات"><MoreVertical size={19} /></button>
        </div>
        <label className="chat-search"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="البحث في المحادثات..." /></label>
        <div className="conversation-list">
          {filtered.map((conversation) => (
            <button key={conversation.id} className={`conversation ${selected.id === conversation.id ? "selected" : ""}`} onClick={() => selectConversation(conversation.id)}>
              <span className="conversation-avatar" style={{ background: conversation.color }}>{conversation.initials}{conversation.online && <i />}</span>
              <span className="conversation-copy"><strong>{conversation.name}</strong><small>{conversation.preview}</small></span>
              <span className="conversation-meta"><time>{conversation.time}</time>{conversation.unread ? <b>{conversation.unread}</b> : null}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="chat-window panel">
        <header className="chat-header">
          <div className="chat-person"><span className="conversation-avatar" style={{ background: selected.color }}>{selected.initials}{selected.online && <i />}</span><div><h2>{selected.name}</h2><span>{selected.online ? "متصل الآن" : selected.role}</span></div></div>
          <div className="chat-actions"><button className="icon-button" aria-label="اتصال صوتي"><Phone size={18} /></button><button className="icon-button" aria-label="مكالمة فيديو"><Video size={20} /></button><button className="icon-button" aria-label="خيارات"><MoreVertical size={19} /></button></div>
        </header>
        <div className="chat-date">اليوم</div>
        <div className="message-list">
          {selected.messages.map((message) => <div key={message.id} className={`message-row ${message.mine ? "mine" : "theirs"}`}><div className="message-bubble"><p>{message.text}</p><span>{message.time} {message.mine && <CheckCheck size={14} className={message.read ? "read" : ""} />}</span></div></div>)}
        </div>
        <div className="chat-composer"><div className="composer-tools"><button className="icon-button" aria-label="إرفاق ملف"><Paperclip size={19} /></button><button className="icon-button" aria-label="إضافة صورة"><Image size={19} /></button><button className="icon-button" aria-label="إضافة رمز تعبيري"><Smile size={19} /></button></div><input value={draft} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") sendMessage(); }} placeholder="اكتب رسالتك هنا..." /><button className="send-button" onClick={sendMessage} aria-label="إرسال الرسالة">{draft.trim() ? <Send size={18} /> : <Mic size={19} />}</button></div>
      </section>
    </div>
  );
}
