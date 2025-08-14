import { FC, useState } from "react";

import styled from "styled-components";
import { Card, Segmented, message } from "antd";
import { LockOutlined, UnlockOutlined } from "@ant-design/icons";

import { AxiosResponse } from "axios";

import { RcFile } from "antd/es/upload";

import { FileUpload } from "../components/FileUpload";
import { FileDownload } from "../components/FileDownload";

import { pdfApi } from "./api";
import { logError } from "../log/logger";
import { ActiveTab, Status, PasswordResponseData } from "./types";

const Main: FC = () => {
	const [messageApi, contextHolder] = message.useMessage();

	// TODO: Move to redux when needed
	// ? File Upload
	const [file, setFile] = useState<RcFile | null>(null);
	const [password, setPassword] = useState<string | null>(null);
	const [activeTab, setActiveTab] = useState<ActiveTab>("lock");

	// ? Fole Download
	const [status, setStatus] = useState<Status>("idle");
	const [result, setResult] = useState<PasswordResponseData | null>(null);

	const handleFileChange = (selectedFile: RcFile | null) => {
		setFile(selectedFile);
	};

	const handlePasswordChange = (selectedPassword: string | null) => {
		setPassword(selectedPassword);
	};

	const handleTabChange = (tab: ActiveTab) => {
		setActiveTab(tab);
	};

	const handleFileProcess = async () => {
		if (!file || !password) {
			messageApi.warning("Please check file and password");
			return;
		}

		if (!password.trim()) {
			messageApi.warning("Please enter the PDF password");
			return;
		}

		setStatus("processing");

		try {
			let response;
			if (activeTab === "lock") {
				response = await pdfApi.lock({ file, password });
			} else {
				response = await pdfApi.unlock({ file, password });
			}

			setResult((response as AxiosResponse<PasswordResponseData>).data);
			setStatus("processed");
			messageApi.success(
				activeTab === "lock" ? "Password added successfully!" : "Password removed successfully!"
			);
		} catch (error: any) {
			logError(`Processing error: ${JSON.stringify(error, null, 2)}`);

			let errorMessage = "An unexpected error occurred";

			if (error.response?.data?.detail.error) {
				errorMessage = error.response.data.detail.error;
			} else if (error.message) {
				errorMessage = error.message;
			}

			setStatus("failed");
			messageApi.error(errorMessage);
		}
	};

	const handleRetry = async () => {
		setStatus("processing");
		setResult(null);

		if (file && password && password.trim()) {
			await handleFileProcess();
		}
	};

	const handleFileDownload = () => {
		if (result) {
			try {
				const { filename, file_data } = result;
				pdfApi.download({ filename, file_data });
				messageApi.success("Download started!");

				setFile(null);
				setResult(null);
				setPassword(null);
				setStatus("idle");
			} catch (error) {
				logError(`Download Error: ${JSON.stringify(error, null, 2)}`);
				messageApi.error("Download Failed, Please Try again!");
			}
		}
	};

	return (
		<>
			{contextHolder}
			<CardContainer variant="borderless">
				<FileContainer>
					<FileUpload
						file={file}
						password={password}
						onFileChange={handleFileChange}
						onPasswordChange={handlePasswordChange}
					/>
				</FileContainer>
				<FileDownload
					status={status}
					retry={handleRetry}
					process={handleFileProcess}
					download={handleFileDownload}
				/>
			</CardContainer>
			<SegmentedContainer
				block
				size="large"
				value={activeTab}
				onChange={(value) => handleTabChange(value as ActiveTab)}
				options={[
					{ label: "Lock", value: "lock", icon: <LockOutlined /> },
					{ label: "Unlock", value: "unlock", icon: <UnlockOutlined /> },
				]}
			/>
		</>
	);
};

export { Main };

const CardContainer = styled(Card)`
	background: transparent;
	padding: 1rem 4rem;

	align-items: center;

	.ant-card-body {
		padding: 0;

		display: flex;
		align-items: center;
		flex-direction: column;

		padding-bottom: 1rem;

		.process {
			width: 14rem;
		}
	}
`;

const FileContainer = styled.div`
	display: flex;
	align-items: center;
	justify-content: stretch;

	gap: 1rem;
`;

const SegmentedContainer = styled(Segmented)`
	align-self: center;
	min-width: 50vw;

	.ant-segmented-group {
		gap: 1rem;
	}
`;
