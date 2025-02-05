import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { messages } = await request.json();

    // TODO: Replace with your actual LLM API call
    // This is just a mock response
    const mockResponse = {
      message: "This is a mock response from the AI. Replace this with your actual LLM integration.",
    };

    return NextResponse.json(mockResponse);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    );
  }
} 