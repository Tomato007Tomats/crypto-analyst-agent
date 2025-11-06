import { NextResponse } from 'next/server';

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
    limit: 500,
  };

  console.log('📤 Making request:', {
    url: requestUrl,
    body: requestBody,
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': `${apiKey.substring(0, 10)}...`,
    },
  });

  try {
    const response = await fetch(requestUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
      },
      body: JSON.stringify(requestBody),
    });

    console.log('📥 Response received:', {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries()),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Store search error:', {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
        url: requestUrl,
      });
      throw new Error(`LangGraph store search failed (${response.status}): ${errorText}`);
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
    console.error('❌ Exception in storeSearch:', error);
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

