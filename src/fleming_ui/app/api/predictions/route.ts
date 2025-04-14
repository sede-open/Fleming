import { TransformData } from "@/helpers/transform-data";
import { NextResponse } from "next/server";

export async function GET(
  request: Request
) {
  try {
    const api = process.env.ML_API;

    // Extract query parameter from URL
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('query');

    // If no query is provided, return an empty array
    if (!query) {
      return NextResponse.json([], { status: 200 });
    }

    const response = await fetch(`${api}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.API_AUTH_TOKEN}`,
        "Content-Type": "application/json",
      },
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

    console.log(data)

    const transformedData = TransformData(data);
    return NextResponse.json(transformedData, { status: 200 });
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json(
        { error: error.message },
        { status: (error.cause as { status?: number })?.status || 500 }
      );
    }

    return NextResponse.json(
      { error: "An unknown error occurred" },
      { status: 500 }
    );
  }
}
