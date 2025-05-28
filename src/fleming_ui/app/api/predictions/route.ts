import { TransformData } from "@/helpers/transform-data";
import { NextResponse } from "next/server";

export async function GET(
  request: Request
) {
  try {
    const customApiUrl = request.headers.get('x-custom-api-url');
    const customAuthToken = request.headers.get('x-custom-auth-token')

    const api = customApiUrl ?? process.env.ML_API;

    const authToken = customApiUrl ? customAuthToken : process.env.API_AUTH_TOKEN;

    // Extract query parameter from URL
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('query');

    // If no query is provided, return an empty array
    if (!query) {
      return NextResponse.json([], { status: 200 });
    }

    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (authToken) {
      headers["Authorization"] = `Bearer ${authToken}`;
    }

    const response = await fetch(`${api}`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        inputs: [query],
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const data = await response.json();

    if (!data) {
      throw new Error("No data received from the API");
    }

    const transformedData = TransformData(data);
    return NextResponse.json(transformedData, { status: 200 });
  } catch (error) {
    if (error instanceof Error) {      return NextResponse.json(
        { error: error.message },
        { status: (error.cause as { status?: number })?.status ?? 500 }
      );
    }

    return NextResponse.json(
      { error: "An unknown error occurred" },
      { status: 500 }
    );
  }
}
