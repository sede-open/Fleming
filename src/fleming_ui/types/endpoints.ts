export interface Endpoint {
  id: string;
  name: string;
  apiUrl: string;
  authToken?: string;
  isDefault?: boolean;
}

export interface EndpointFormData {
  name: string;
  apiUrl: string;
  authToken?: string;
}
