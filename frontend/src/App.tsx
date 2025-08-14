import { FC } from "react";

import styled from "styled-components";
import { Image, Layout } from "antd";

import { ThemeProvider } from "./theme/ThemeProvider";

import { Main } from "./containers/Main";

import LogoSvg from "./asset/logo.svg";

const { Header, Content, Footer } = Layout;

const App: FC = () => {
	return (
		<>
			<ThemeProvider>
				<LayoutContainer>
					<HeaderContainer>
						<ImageContainer src={LogoSvg} alt="Logo" preview={false} width={48} />
						Papyrus
					</HeaderContainer>
					<ContentContainer>
						<Main />
					</ContentContainer>
					<FooterContainer>⬜️ Papyrus - Secure, Fast and Privacy-First ⬜️</FooterContainer>
				</LayoutContainer>
			</ThemeProvider>
		</>
	);
};

export { App };

const LayoutContainer = styled(Layout)`
	width: 100%;
	min-height: 100vh;
`;

const HeaderContainer = styled(Header)`
	height: 10vh;
	padding: 2rem 4rem;
	background: transparent;

	display: flex;
	align-items: center;
	justify-content: center;

	font-size: 2.5rem;
	font-weight: bolder;
	box-shadow: 0 4px 8px -2px rgba(255, 255, 255, 0.15);
`;

const ImageContainer = styled(Image)`
	padding-right: 1rem;
`;

const ContentContainer = styled(Content)`
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	align-items: stretch;
	justify-content: center;
`;

const FooterContainer = styled(Footer)`
	height: 10vh;

	display: flex;
	align-items: center;
	justify-content: center;

	font-weight: lighter;
	box-shadow: 0 -4px 8px -2px rgba(255, 255, 255, 0.15);
`;
