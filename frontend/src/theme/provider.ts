import { ThemeConfig } from "antd";

const DarkThemeProvider: ThemeConfig = {
	token: {
		colorPrimary: "#ffffff", // Use white as the primary color in dark mode
		fontFamily:
			"Outfit, Onest, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif",
		colorBgBase: "#121212", // Dark background
		colorTextBase: "#ffffff", // White text
	},
	components: {
		Button: {
			algorithm: true,
			primaryShadow: "none",
			boxShadowSecondary: "none",
			boxShadowTertiary: "none",
			dangerShadow: "none",
			defaultShadow: "none",
		},
		Card: {
			colorBorderSecondary: "#ffffff33", // Subtle border color for dark mode
			headerBg: "#1e1e1e", // Darker header background
		},
		Input: {
			activeShadow: "none",
		},
		InputNumber: {
			activeShadow: "none",
		},
		Typography: {
			linkDecoration: "overline",
			colorLink: "#ffffff", // White links for dark mode
			colorLinkActive: "#ffffffcc", // Slightly dimmed white
			colorLinkHover: "#ffffff", // Bright white hover effect
		},
		Divider: {
			colorSplit: "#ffffff44", // Subtle divider color
		},
		Tabs: {
			itemColor: "#ffffff88", // Dimmed white for inactive tabs
			itemHoverColor: "#ffffffcc", // Brighter white on hover
		},
		Menu: {
			itemSelectedBg: "#ffffff", // Bright selection background
			itemSelectedColor: "#000000", // Contrast with selection background
			itemColor: "#ffffff88", // Dimmed white for unselected items
			itemHoverColor: "#ffffffcc", // Brighter white on hover
		},
		Select: {
			optionSelectedBg: "#ffffff", // Bright background for selected options
			optionSelectedColor: "#000000", // Black text for contrast
			optionSelectedFontWeight: 300,
			colorTextQuaternary: "#ffffff88", // Dimmed white for inactive text
		},
		Segmented: {
			itemSelectedBg: "#ffffff", // Bright background for selected items
			itemSelectedColor: "#000000", // Contrast with selection background
		},
	},
};

export { DarkThemeProvider };
