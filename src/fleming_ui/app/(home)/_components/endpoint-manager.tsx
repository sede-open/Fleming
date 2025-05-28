"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
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
import { Endpoint, EndpointFormData } from "@/types/endpoints";

interface EndpointManagerProps {
  readonly endpoints: Endpoint[];
  readonly onEndpointsChange: (endpoints: Endpoint[]) => void;
}

export default function EndpointManager({ endpoints, onEndpointsChange }: EndpointManagerProps) {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState<EndpointFormData>({
    name: "",
    apiUrl: "",
    authToken: ""
  });

  const resetForm = () => {
    setFormData({
      name: "",
      apiUrl: "",
      authToken: ""
    });
  };

  const handleOpen = () => {
    resetForm();
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    resetForm();
  };

  const handleSubmit = () => {
    if (!formData.name.trim() || !formData.apiUrl.trim()) {
      return;
    }

    const newEndpoint: Endpoint = {
      id: `endpoint-${Date.now()}`,
      name: formData.name,
      apiUrl: formData.apiUrl,
      authToken: formData.authToken ?? undefined,
      isDefault: false
    };
    onEndpointsChange([...endpoints, newEndpoint]);

    handleClose();
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="gap-2"
          onClick={() => handleOpen()}
        >
          <Plus className="h-4 w-4" />
          Add Endpoint
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Endpoint</DialogTitle>
          <DialogDescription>
            Add a new ML API endpoint to search across multiple sources.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="endpoint-name">Name *</Label>
            <Input
              id="endpoint-name"
              placeholder="e.g., Production API"
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            />
            <p className="text-xs text-muted-foreground">
              A descriptive name for this endpoint
            </p>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="endpoint-url">API URL *</Label>
            <Input
              id="endpoint-url"
              placeholder="https://your-api-endpoint.com"
              value={formData.apiUrl}
              onChange={(e) => setFormData(prev => ({ ...prev, apiUrl: e.target.value }))}
            />
            <p className="text-xs text-muted-foreground">
              The full URL to the ML API endpoint
            </p>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="endpoint-token">Auth Token (Optional)</Label>
            <Input
              id="endpoint-token"
              type="password"
              placeholder="your-auth-token"
              value={formData.authToken}
              onChange={(e) => setFormData(prev => ({ ...prev, authToken: e.target.value }))}
            />
            <p className="text-xs text-muted-foreground">
              Leave empty if no authentication is required
            </p>
          </div>
        </div>
        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={handleClose}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={!formData.name.trim() || !formData.apiUrl.trim()}
          >
            Add Endpoint
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
