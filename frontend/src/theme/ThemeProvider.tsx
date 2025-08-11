import { FC, PropsWithChildren, createContext } from "react";
import { ConfigProvider } from "antd";

import { DarkThemeProvider } from "./provider";

// Context to Share Theme State
const ThemeContext = createContext({
	theme: "dark", // Default theme
});

const ThemeProvider: FC<PropsWithChildren> = ({ children }) => {
	return (
		<ThemeContext.Provider value={{ theme: "dark" }}>
			<ConfigProvider theme={DarkThemeProvider}>{children}</ConfigProvider>
		</ThemeContext.Provider>
	);
};

export { ThemeProvider };
