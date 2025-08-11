import { FC } from "react";

import { Image, Layout } from "antd";

import { ThemeProvider } from "./theme/ThemeProvider";

import LogoSvg from "./asset/logo.svg";

const { Header, Content, Footer } = Layout;

const App: FC = () => {
	return (
		<>
			<ThemeProvider>
				<Layout style={{ minHeight: "100vh", width: "100%" }}>
					<Header
						style={{
							height: "10vh",
							padding: "2rem 4rem",
							background: "transparent",
							boxShadow: "0 4px 8px -2px rgba(255, 255, 255, 0.15)",

							display: "flex",
							alignItems: "center",
							justifyContent: "center",

							fontSize: "2.5rem",
							fontWeight: "bolder",
						}}
					>
						<Image
							src={LogoSvg}
							alt="Logo"
							preview={false}
							width={48}
							style={{ paddingRight: "1rem" }}
						/>
						Papyrus
					</Header>
					<Content style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
						Main Body
					</Content>
					<Footer
						style={{
							height: "10vh",
							boxShadow: "0 -4px 8px -2px rgba(255, 255, 255, 0.15)",

							display: "flex",
							alignItems: "center",
							justifyContent: "center",

							fontWeight: "lighter",
						}}
					>
						⬜️ Papyrus - Secure, Fast and Privacy-First ⬜️
					</Footer>
				</Layout>
			</ThemeProvider>
		</>
	);
};

export { App };
