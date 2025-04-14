"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Greetings from "./components/greetings";
import Search from "./components/search";
import Filters from "./components/filter";
import Results, { Result } from "./components/result";
import useSWR from 'swr';
import fetcher from "@/utils/fetcher";
import Loading from "./components/loading";
import Error from "./components/error";

export default function Home() {
  const [showFilters, setShowFilters] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [sort, setSort] = useState("score");

  const { data, error, isLoading } = useSWR(
    searchQuery ? `/api/predictions?query=${encodeURIComponent(searchQuery)}` : null,
    fetcher,
    {
      revalidateOnFocus: false,
      refreshInterval: 0,
      shouldRetryOnError: false
    }
  );

  const results = searchQuery ? (data || []) : [];

  return (
    <div className="flex flex-col">
      <Greetings />
      <Search setShowFilters={setShowFilters} setSearchQuery={setSearchQuery} />

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
