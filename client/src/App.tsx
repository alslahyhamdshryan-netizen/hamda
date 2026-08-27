import { useState } from "react";
import { Bell, ChevronDown, CircleDollarSign, FileBarChart2, LayoutDashboard, LogOut, Menu, Settings, Users, WalletCards, X } from "lucide-react";
import Home from "@/pages/Home";

export default function App() {
  const [active, setActive] = useState("الرئيسية");
  const [open, setOpen] = useState(false);
  const items = [
    ["الرئيسية", LayoutDashboard],
    ["العمليات", WalletCards],
    ["العملاء", Users],
    ["الأسعار", CircleDollarSign],
    ["التقارير", FileBarChart2],
  ] as const;
  return (
    <div className="app-shell" dir="rtl">
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="brand"><div className="brand-mark">ص</div><div><strong>صَرافة</strong><span>نظام إدارة الصراف</span></div><button className="mobile-close" onClick={() => setOpen(false)}><X size={18}/></button></div>
        <div className="branch-card"><span className="status-dot"/> فرع السوق المركزي <ChevronDown size={14}/></div>
        <nav>{items.map(([label, Icon]) => <button key={label} className={active === label ? "nav-item active" : "nav-item"} onClick={() => { setActive(label); setOpen(false); }}><Icon size={18}/><span>{label}</span>{label === "العمليات" && <b>3</b>}</button>)}</nav>
        <div className="nav-bottom"><button className="nav-item"><Settings size={18}/><span>الإعدادات</span></button><button className="nav-item"><LogOut size={18}/><span>تسجيل الخروج</span></button></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><button className="mobile-menu" onClick={() => setOpen(true)}><Menu size={21}/></button><div><p className="eyebrow">الخميس، ٢٧ أغسطس ٢٠٢٦</p><h1>{active}</h1></div><div className="top-actions"><button className="icon-button notification"><Bell size={19}/><i/></button><div className="user-menu"><div className="avatar">م</div><div className="user-name"><strong>محمد أحمد</strong><span>أمين الصندوق</span></div><ChevronDown size={16}/></div></div></header>
        <Home />
      </main>
    </div>
  );
}
