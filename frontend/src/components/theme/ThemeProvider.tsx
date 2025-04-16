"use client";

import { ThemeProvider as NextThemesProvider, type ThemeProviderProps } from "next-themes";

const ThemeProvider = ({ children, ...props }: ThemeProviderProps) => {
	return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
};

export { ThemeProvider };
