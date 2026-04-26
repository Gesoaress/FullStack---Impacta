import { createContext, useContext, useState, useCallback } from 'react';

const Ctx = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken]   = useState(() => localStorage.getItem('token'));
  const [seller, setSeller] = useState(() => { try { return JSON.parse(localStorage.getItem('seller')); } catch { return null; } });

  const signIn = useCallback((t, s) => {
    localStorage.setItem('token', t);
    localStorage.setItem('seller', JSON.stringify(s));
    setToken(t); setSeller(s);
  }, []);

  const signOut = useCallback(() => {
    localStorage.removeItem('token'); localStorage.removeItem('seller');
    setToken(null); setSeller(null);
  }, []);

  return (
    <Ctx.Provider value={{ token, seller, signIn, signOut, isAuthenticated: !!token }}>
      {children}
    </Ctx.Provider>
  );
}

export const useAuth = () => {
  const c = useContext(Ctx);
  if (!c) throw new Error('useAuth must be inside AuthProvider');
  return c;
};