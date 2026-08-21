/** Design: Warm Code Studio — local, privacy-friendly progress tracking without a backend. */
import { useEffect, useMemo, useState } from "react";

const WATCHED_STORAGE_KEY = "flutter-shorts-watched-videos";

export function useWatchedVideos() {
  const [watchedIds, setWatchedIds] = useState<string[]>([]);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(WATCHED_STORAGE_KEY);
      if (saved) setWatchedIds(JSON.parse(saved));
    } catch {
      setWatchedIds([]);
    }
  }, []);

  const updateWatched = (next: string[]) => {
    setWatchedIds(next);
    try {
      window.localStorage.setItem(WATCHED_STORAGE_KEY, JSON.stringify(next));
    } catch {
      // Keep the in-session state when local storage is unavailable.
    }
  };

  const toggleWatched = (id: string) => {
    updateWatched(watchedIds.includes(id) ? watchedIds.filter((watchedId) => watchedId !== id) : [...watchedIds, id]);
  };

  const progressLabel = useMemo(() => `${watchedIds.length} حلقة مكتملة`, [watchedIds.length]);

  return { watchedIds, toggleWatched, progressLabel };
}
