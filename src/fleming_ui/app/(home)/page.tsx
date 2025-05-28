"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import Greetings from "./_components/greetings";
import Search from "./_components/search";
import Filters from "./_components/filter";
import Results, { Result } from "./_components/result";
import Loading from "./_components/loading";
import Error from "./_components/error";
import EndpointManager from "./_components/endpoint-manager";
import useSWR from 'swr';
import { createCustomFetcher } from "@/utils/custom-fetcher";
import { Endpoint } from "@/types/endpoints";

export default function Home() {
  const [showFilters, setShowFilters] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [sort, setSort] = useState("score");
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);  const [activeEndpoint, setActiveEndpoint] = useState<string>("");

  useEffect(() => {
    const savedEndpoints = localStorage.getItem("mlEndpoints");
    if (savedEndpoints) {
      const parsedEndpoints = JSON.parse(savedEndpoints);
      setEndpoints(parsedEndpoints);

      const defaultEndpoint = parsedEndpoints.find((ep: Endpoint) => ep.isDefault);
      setActiveEndpoint(defaultEndpoint?.id ?? parsedEndpoints[0]?.id ?? "");
    } else {
      const defaultEndpoint: Endpoint = {
        id: "default",
        name: "Default Endpoint",
        apiUrl: "",
        isDefault: true
      };
      setEndpoints([defaultEndpoint]);
      setActiveEndpoint("default");
      localStorage.setItem("mlEndpoints", JSON.stringify([defaultEndpoint]));
    }
  }, []);

  const activeEndpointData = endpoints.find(ep => ep.id === activeEndpoint);
  const customSettings = activeEndpointData ? {
    customApiUrl: activeEndpointData.apiUrl ?? undefined,
    customAuthToken: activeEndpointData.authToken ?? undefined,
  } : {};  const customFetcher = createCustomFetcher(customSettings);

  const cacheKey = searchQuery && activeEndpoint
    ? `${activeEndpoint}:${searchQuery}`
    : null;

  const { data: results = [], error, isLoading } = useSWR(
    cacheKey,
    () => customFetcher(`/api/predictions?query=${encodeURIComponent(searchQuery)}`),
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 0,
      dedupingInterval: 2000,
      shouldRetryOnError: false,
      keepPreviousData: true,
    }
  );
  const handleEndpointsChange = useCallback((newEndpoints: Endpoint[]) => {
    setEndpoints(newEndpoints);
    localStorage.setItem("mlEndpoints", JSON.stringify(newEndpoints));

    if (!newEndpoints.find(ep => ep.id === activeEndpoint)) {
      const defaultEndpoint = newEndpoints.find(ep => ep.isDefault);
      setActiveEndpoint(defaultEndpoint?.id ?? newEndpoints[0]?.id ?? "");
    }  }, [activeEndpoint]);

  const handleRemoveEndpoint = (endpointId: string) => {
    if (endpoints.find(ep => ep.id === endpointId)?.isDefault) {
      return;
    }

    const newEndpoints = endpoints.filter(ep => ep.id !== endpointId);
    handleEndpointsChange(newEndpoints);
  };

  return (
    <div className="flex flex-col">
      <Greetings />

      <Search
        setShowFilters={setShowFilters}
        setSearchQuery={setSearchQuery}
      />

      <div className="mt-6 mb-4">
        <Tabs value={activeEndpoint} onValueChange={setActiveEndpoint}>
          <div className="flex items-center justify-between border-b border-border pb-4 mb-6">
            <div className="flex items-center space-x-4">
              <h3 className="text-sm font-medium text-muted-foreground">Search Endpoints:</h3>              <TabsList className="h-10 p-1 bg-muted/50">
                {endpoints.map((endpoint) => (
                  <TabsTrigger
                    key={endpoint.id}
                    value={endpoint.id}
                    className="group relative px-3 py-2 text-sm font-medium transition-all data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm"
                  >
                    <div className="flex items-center justify-between gap-2 min-w-0">
                      <span className="truncate">{endpoint.name}</span>
                      {!endpoint.isDefault && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-4 w-4 p-2
                          text-muted-foreground
                          hover:bg-destructive/20 hover:text-destructive shrink-0"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleRemoveEndpoint(endpoint.id);
                          }}
                        >
                          <X className="h-3 w-3" />
                        </Button>
                      )}
                    </div>
                  </TabsTrigger>
                ))}
              </TabsList>
            </div>
            <EndpointManager
              endpoints={endpoints}
              onEndpointsChange={handleEndpointsChange}
            />
          </div>

          {endpoints.map((endpoint) => (
            <TabsContent key={endpoint.id} value={endpoint.id} className="mt-0">
              <div className="space-y-6">
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
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  );
}
