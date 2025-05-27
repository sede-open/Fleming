// Custom fetcher that supports advanced settings headers
export const createCustomFetcher = (customSettings?: { customApiUrl?: string; customAuthToken?: string }) => {
  return async (url: string) => {
    const headers: Record<string, string> = {};

    // Add custom headers if settings are provided
    if (customSettings?.customApiUrl) {
      headers['x-custom-api-url'] = customSettings.customApiUrl;
    }

    if (customSettings?.customAuthToken) {
      headers['x-custom-auth-token'] = customSettings.customAuthToken;
    }

    const response = await fetch(url, {
      headers: Object.keys(headers).length > 0 ? headers : undefined,
    });

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    return response.json();
  };
};

// Default fetcher (keeping the original for backward compatibility)
const fetcher = async (url: string) => {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }

  return response.json();
};

export default fetcher;
