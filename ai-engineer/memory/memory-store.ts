interface UserContext {
  lastMessage?: string;
  lastResponse?: string;
  lastToolCalls?: unknown[];
  preferences?: Record<string, unknown>;
  history?: unknown[];
}

const store = new Map<string, UserContext>();

export const memoryStore = {
  getUserContext: async (userId: string): Promise<UserContext> => {
    return store.get(userId) || {};
  },

  updateUserContext: async (userId: string, context: Partial<UserContext>): Promise<void> => {
    const existing = store.get(userId) || {};
    store.set(userId, { ...existing, ...context });
  },

  addInteraction: async (userId: string, interaction: unknown): Promise<void> => {
    const existing = store.get(userId) || {};
    const history = existing.history || [];
    history.push(interaction);
    store.set(userId, { ...existing, history });
  },

  clearUserContext: async (userId: string): Promise<void> => {
    store.delete(userId);
  },
};
