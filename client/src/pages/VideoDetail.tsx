/**
 * Design: Warm Code Studio — a focused editorial lesson page for one video, script, code, and watch state.
 */
import { useState } from "react";
import { Link, useRoute } from "wouter";
import { ArrowRight, Check, Clock3, Code2, Copy, Play, TerminalSquare } from "lucide-react";
import { getVideoById } from "@/lib/videos";
import { useWatchedVideos } from "@/hooks/useWatchedVideos";

const asset = (name: string) => `${import.meta.env.BASE_URL}assets/${name}`;
const featuredVideo = asset("flutter-pubspec-captioned_0bc857a6.mp4");
const providerImage = asset("flutter-provider-scene_7150ecab.png");
const brandMark = asset("flutter-shorts-mark_6acf0d64.png");

export default function VideoDetail() {
  const [, params] = useRoute("/videos/:id");
  const video = getVideoById(params?.id ?? "");
  const { watchedIds, toggleWatched } = useWatchedVideos();
  const [copied, setCopied] = useState(false);

  if (!video) {
    return (
      <div className="min-h-screen bg-[#111315] px-5 py-20 text-white" dir="rtl">
        <Link href="/" className="inline-flex items-center gap-2 text-[#F2A04B]"><ArrowRight className="h-4 w-4" /> العودة إلى الأرشيف</Link>
        <h1 className="mt-8 font-plex text-4xl font-bold">لم نعثر على هذه الحلقة.</h1>
      </div>
    );
  }

  const watched = watchedIds.includes(video.id);
  const tone = video.accent === "amber" ? "#F2A04B" : video.accent === "blue" ? "#47B8FF" : "#FF6A5A";

  const copyCode = async () => {
    await navigator.clipboard.writeText(video.code);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className="min-h-screen bg-[#111315] text-[#F8F4EE]" dir="rtl">
      <div className="pointer-events-none fixed inset-0 studio-noise" aria-hidden="true" />
      <header className="relative z-10 mx-auto flex max-w-[1320px] items-center justify-between px-5 py-5 sm:px-8 lg:px-12">
        <Link href="/" className="flex items-center gap-3"><img src={brandMark} alt="Hamed Flutter" className="h-10 w-10 object-contain" /><span className="font-plex text-lg font-bold">Hamed Flutter <small className="mr-2 font-mono text-[9px] tracking-[0.16em] text-[#F2A04B]">CODE STUDIO</small></span></Link>
        <Link href="/#archive" className="inline-flex items-center gap-2 text-sm font-bold text-white/70 transition hover:text-[#F2A04B]"><ArrowRight className="h-4 w-4" /> كل الحلقات</Link>
      </header>

      <main className="relative z-10 mx-auto max-w-[1320px] px-5 pb-20 sm:px-8 lg:px-12">
        <section className="grid gap-10 border-b border-white/10 pb-14 pt-10 lg:grid-cols-[0.88fr_1.12fr] lg:items-center lg:pt-16">
          <div className="overflow-hidden border border-white/10 bg-[#090B0D]">
            {video.available ? (
              <video className="aspect-[9/16] w-full object-cover" controls preload="metadata" poster={providerImage}><source src={featuredVideo} type="video/mp4" />متصفحك لا يدعم تشغيل الفيديو.</video>
            ) : (
              <div className="relative aspect-[9/16] overflow-hidden"><img src={providerImage} alt="غلاف حلقة Flutter" className="h-full w-full object-cover" /><div className="absolute inset-0 bg-[linear-gradient(180deg,transparent,rgba(17,19,21,.9))]" /><div className="absolute bottom-0 right-0 left-0 p-6"><span className="border px-2 py-1 font-mono text-[10px]" style={{ borderColor: tone, color: tone }}>SCRIPT READY</span><p className="mt-4 font-plex text-2xl font-bold">حلقة قيد الإنتاج — ابدأ من السكربت والكود.</p></div></div>
            )}
          </div>

          <div>
            <div className="mb-7 flex flex-wrap items-center gap-3"><span className="border px-3 py-1.5 font-mono text-[10px] tracking-[0.12em]" style={{ borderColor: tone, color: tone }}>{video.signal}</span><span className="font-mono text-[11px] text-white/40">{video.duration} · {video.topic}</span></div>
            <p className="font-mono text-[11px] tracking-[0.15em] text-[#F2A04B]">إعداد وتقديم: م/ حامد شريان</p>
            <h1 className="mt-4 font-plex text-4xl font-bold leading-tight text-white sm:text-5xl">{video.title}</h1>
            <p className="mt-6 max-w-[660px] text-lg leading-8 text-white/65">{video.description}</p>
            <div className="mt-8 flex flex-wrap gap-4">
              <button onClick={() => toggleWatched(video.id)} className={`inline-flex items-center gap-3 px-5 py-3 text-sm font-bold transition active:scale-[0.97] ${watched ? "bg-[#47B8FF] text-[#07141D]" : "bg-[#F2A04B] text-[#17130E] hover:bg-[#FFC26D]"}`}>
                <Check className="h-4 w-4" /> {watched ? "تمت مشاهدتها" : "تحديد كتمت مشاهدتها"}
              </button>
              <a href="#script" className="inline-flex items-center gap-2 border border-white/15 px-5 py-3 text-sm font-bold text-white/75 transition hover:border-[#47B8FF]/60 hover:text-white"><Play className="h-4 w-4" /> انتقل إلى السكربت</a>
            </div>
            <div className="mt-10 border-r-2 pr-5 text-sm leading-7 text-white/60" style={{ borderColor: tone }}><span className="font-bold text-white">الخلاصة:</span> {video.takeaway}</div>
          </div>
        </section>

        <section id="script" className="grid gap-10 py-16 lg:grid-cols-[0.8fr_1.2fr]">
          <div><p className="font-mono text-[11px] tracking-[0.15em] text-[#F2A04B]">PRESENTER SCRIPT</p><h2 className="mt-3 font-plex text-3xl font-bold">نص جاهز للشرح</h2><p className="mt-4 leading-8 text-white/55">اقرأ الفقرات بالترتيب في فيديو قصير، أو استخدمها كنقطة بداية لحلقة أطول.</p></div>
          <div className="divide-y divide-white/10 border-y border-white/10">
            {video.script.map((paragraph, index) => <p key={paragraph} className="py-5 text-base leading-8 text-white/75"><span className="ml-3 font-mono text-xs" style={{ color: tone }}>{String(index + 1).padStart(2, "0")}</span>{paragraph}</p>)}
          </div>
        </section>

        <section className="grid gap-10 border-t border-white/10 py-16 lg:grid-cols-[0.8fr_1.2fr]">
          <div><p className="font-mono text-[11px] tracking-[0.15em] text-[#47B8FF]">CODE STARTER</p><h2 className="mt-3 font-plex text-3xl font-bold">مثال قابل للنسخ</h2><p className="mt-4 leading-8 text-white/55">ابدأ من هذا المثال ثم عدّله ليناسب بنية مشروعك الحقيقي.</p></div>
          <div className="overflow-hidden border border-white/10 bg-[#090B0D]">
            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4"><span className="inline-flex items-center gap-2 font-mono text-xs text-white/70"><TerminalSquare className="h-4 w-4 text-[#47B8FF]" />flutter-snippet.dart</span><button onClick={copyCode} className="inline-flex items-center gap-2 text-xs font-bold text-[#F2A04B]">{copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}{copied ? "تم النسخ" : "نسخ الكود"}</button></div>
            <pre dir="ltr" className="overflow-x-auto p-6 text-left font-mono text-[12px] leading-6 text-[#DDEAF1]"><code>{video.code}</code></pre>
          </div>
        </section>
      </main>
    </div>
  );
}
