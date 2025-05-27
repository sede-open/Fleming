"use client";

import { useState, useEffect } from "react";
import { Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface AdvancedSettingsProps {
  readonly onSettingsChange: (settings: { customApiUrl?: string; customAuthToken?: string }) => void;
}

export default function AdvancedSettings({ onSettingsChange }: AdvancedSettingsProps) {
  const [open, setOpen] = useState(false);
  const [customApiUrl, setCustomApiUrl] = useState("");
  const [customAuthToken, setCustomAuthToken] = useState("");
  const [isUsingCustomSettings, setIsUsingCustomSettings] = useState(false);

  // Load settings from localStorage on component mount
  useEffect(() => {
    const savedApiUrl = localStorage.getItem("customApiUrl");
    const savedAuthToken = localStorage.getItem("customAuthToken");

    if (savedApiUrl) {
      setCustomApiUrl(savedApiUrl);
      setIsUsingCustomSettings(true);
    }
    if (savedAuthToken) {
      setCustomAuthToken(savedAuthToken);
    }

    // Notify parent component of existing settings (only on mount)
    if (savedApiUrl || savedAuthToken) {
      onSettingsChange({
        customApiUrl: savedApiUrl ?? undefined,
        customAuthToken: savedAuthToken ?? undefined,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Remove onSettingsChange from dependency array to prevent infinite loop

  const handleSave = () => {
    // Save to localStorage
    if (customApiUrl) {
      localStorage.setItem("customApiUrl", customApiUrl);
    } else {
      localStorage.removeItem("customApiUrl");
    }

    if (customAuthToken) {
      localStorage.setItem("customAuthToken", customAuthToken);
    } else {
      localStorage.removeItem("customAuthToken");
    }

    setIsUsingCustomSettings(!!customApiUrl);

    // Notify parent component
    onSettingsChange({
      customApiUrl: customApiUrl || undefined,
      customAuthToken: customAuthToken || undefined,
    });

    setOpen(false);
  };

  const handleReset = () => {
    setCustomApiUrl("");
    setCustomAuthToken("");
    localStorage.removeItem("customApiUrl");
    localStorage.removeItem("customAuthToken");
    setIsUsingCustomSettings(false);

    onSettingsChange({});
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="outline"
          className={`gap-2 h-full ${isUsingCustomSettings ? 'border-blue-500 text-blue-600' : ''}`}
        >
          <Settings className="h-4 w-4" />
          Advanced
          {isUsingCustomSettings && (
            <span className="h-2 w-2 rounded-full bg-blue-500"></span>
          )}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Advanced Settings</DialogTitle>
          <DialogDescription>
            Configure your custom ML API settings. Leave fields empty to use default values.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="api-url">Custom API URL</Label>
            <Input
              id="api-url"
              placeholder="https://your-api-endpoint.com"
              value={customApiUrl}
              onChange={(e) => setCustomApiUrl(e.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              Override the default ML API endpoint
            </p>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="auth-token">Custom Auth Token</Label>
            <Input
              id="auth-token"
              type="password"
              placeholder="your-auth-token"
              value={customAuthToken}
              onChange={(e) => setCustomAuthToken(e.target.value)}
              showPasswordToggle={true}
            />
            <p className="text-xs text-muted-foreground">
              Optional: Override the default Bearer authentication token
            </p>
          </div>
        </div>
        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={handleReset}>
            Reset to Default
          </Button>
          <Button onClick={handleSave}>Save Settings</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
