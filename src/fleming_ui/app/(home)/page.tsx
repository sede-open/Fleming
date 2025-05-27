"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Greetings from "./_components/greetings";
import Search from "./_components/search";
import Filters from "./_components/filter";
import Results, { Result } from "./_components/result";
import useSWR from 'swr';
import { createCustomFetcher } from "@/utils/custom-fetcher";
import Loading from "./_components/loading";
import Error from "./_components/error";

export default function Home() {
  const [showFilters, setShowFilters] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [sort, setSort] = useState("score");
  const [customSettings, setCustomSettings] = useState<{ customApiUrl?: string; customAuthToken?: string }>({});

  // Create custom fetcher with current settings
  const customFetcher = createCustomFetcher(customSettings);
  // Create a unique cache key that includes custom settings
  const cacheKey = searchQuery
    ? JSON.stringify({
        url: `/api/predictions?query=${encodeURIComponent(searchQuery)}`,
        customApiUrl: customSettings.customApiUrl,
        customAuthToken: customSettings.customAuthToken
      })
    : null;

  const { data, error, isLoading } = useSWR(
    cacheKey,
    () => customFetcher(`/api/predictions?query=${encodeURIComponent(searchQuery)}`),
    {
      revalidateOnFocus: false,
      refreshInterval: 0,
      shouldRetryOnError: false
    }
  );

  const results = searchQuery ? (data ?? []) : [];

  const handleAdvancedSettingsChange = useCallback((settings: { customApiUrl?: string; customAuthToken?: string }) => {
    setCustomSettings(settings);
  }, []);

  return (
    <div className="flex flex-col">
      <Greetings />
      <Search
        setShowFilters={setShowFilters}
        setSearchQuery={setSearchQuery}
        onAdvancedSettingsChange={handleAdvancedSettingsChange}
      />

      {/* Animated Filters */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.1 }}
            style={{ overflow: "hidden" }}
          >
            <Filters setSort={setSort} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Animated Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Error />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Animated Loading/Results */}
      <AnimatePresence mode="wait">
        {isLoading ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Loading />
          </motion.div>
        ) : (
          <motion.div
            key="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.3 }}
          >
            <Results results={sort === 'alpha' ? results.sort(
              (a: Result, b: Result) => a.name.localeCompare(b.name)) : results.sort(
                (a: Result, b: Result) => b.score - a.score)} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
