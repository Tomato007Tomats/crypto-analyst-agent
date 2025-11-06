import { NextResponse } from 'next/server';

// Force dynamic rendering - this route needs to fetch data at request time
export const dynamic = 'force-dynamic';
export const revalidate = 0;
export const maxDuration = 60; // Maximum duration in seconds (Vercel Pro: up to 300s)

const LANGSMITH_API_URL = process.env.LANGSMITH_API_URL;
const LANGSMITH_API_KEY = process.env.LANGSMITH_API_KEY;
const STORE_NAMESPACE = ['opportunities'];

interface StoreSearchResponse {
  items?: Array<{
    namespace: string[];
    key: string;
    value: Record<string, unknown>;
  }>;
}

async function storeSearch(): Promise<Record<string, unknown>[]> {
  console.log('🔍 Starting store search...');
  console.log('Environment check:', {
    hasApiUrl: !!LANGSMITH_API_URL,
    hasApiKey: !!LANGSMITH_API_KEY,
    apiUrl: LANGSMITH_API_URL,
  });

  if (!LANGSMITH_API_URL || !LANGSMITH_API_KEY) {
    console.error('❌ Missing LangSmith configuration');
    throw new Error('Missing LangSmith configuration');
  }

  const apiUrl = LANGSMITH_API_URL;
  const apiKey = LANGSMITH_API_KEY;
  const requestUrl = `${apiUrl}/store/search`;
  const requestBody = {
    namespace_prefix: STORE_NAMESPACE,
    limit: 50, // Reduced from 500 to avoid Vercel 4.5MB limit
    offset: 0,
  };

  console.log('📤 Making request:', {
    url: requestUrl,
    body: requestBody,
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Key': `${apiKey.substring(0, 10)}...`,
    },
  });

  // Add timeout handling
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds

  try {
    const response = await fetch(requestUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Api-Key': apiKey, // Uppercase as per LangGraph Server API docs
        'Accept': 'application/json',
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    console.log('📥 Response received:', {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries()),
    });

    if (!response.ok) {
      let errorDetails;
      const contentType = response.headers.get('content-type');

      try {
        if (contentType?.includes('application/json')) {
          errorDetails = await response.json();
        } else {
          errorDetails = await response.text();
        }
      } catch (e) {
        errorDetails = 'Could not parse error response';
      }

      const errorInfo = {
        status: response.status,
        statusText: response.statusText,
        url: requestUrl,
        requestBody: requestBody,
        errorDetails: errorDetails,
        headers: Object.fromEntries(response.headers.entries()),
        timestamp: new Date().toISOString(),
      };

      console.error('❌ Store search error:', JSON.stringify(errorInfo, null, 2));
      throw new Error(`LangGraph store search failed: ${JSON.stringify(errorInfo)}`);
    }

    const payload = (await response.json()) as StoreSearchResponse;
    console.log('✅ Response parsed:', {
      itemCount: payload.items?.length ?? 0,
      items: payload.items,
    });

    const items = payload.items ?? [];

    const filtered = items
      .filter((item) => Array.isArray(item.namespace) && item.namespace.join() === STORE_NAMESPACE.join())
      .map((item) => ({ ...item.value, id: item.key }));

    console.log('✅ Filtered opportunities:', {
      count: filtered.length,
      opportunities: filtered,
    });

    return filtered;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof Error && error.name === 'AbortError') {
      console.error('❌ Request timeout after 30 seconds');
      throw new Error('Request timeout - LangGraph API took too long to respond');
    }

    console.error('❌ Exception in storeSearch:', {
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
      timestamp: new Date().toISOString(),
    });
    throw error;
  }
}

export async function GET() {
  try {
    const opportunities = await storeSearch();

    opportunities.sort((a, b) => {
      const createdA = typeof a.created_at === 'string' ? a.created_at : '';
      const createdB = typeof b.created_at === 'string' ? b.created_at : '';
      return createdA.localeCompare(createdB);
    });

    return NextResponse.json({ opportunities });
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    return NextResponse.json(
      { error: 'Failed to fetch opportunities' },
      { status: 500 }
    );
  }
}

