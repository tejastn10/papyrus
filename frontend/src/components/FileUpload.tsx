import { FC } from "react";

import styled from "styled-components";
import { Upload, Flex, Typography, Input, message } from "antd";
import { InboxOutlined, LockOutlined } from "@ant-design/icons";

import { RcFile } from "antd/es/upload";

import { isPdfFile, isValidFileSize } from "./utils";

const { Dragger } = Upload;
const { Title, Text } = Typography;

interface Props {
	file: RcFile | null;
	password: string | null;

	onFileChange: (file: RcFile | null) => void;
	onPasswordChange: (password: string | null) => void;
}

const FileUpload: FC<Props> = ({ password, onPasswordChange, file, onFileChange }) => {
	const [messageApi, contextHolder] = message.useMessage();

	const uploadProps = {
		name: "file",
		multiple: false,
		accept: ".pdf",
		beforeUpload: (file: RcFile) => {
			if (!isPdfFile(file)) {
				messageApi.error("Only PDF files are allowed");
				return Upload.LIST_IGNORE;
			}

			if (!isValidFileSize(file)) {
				messageApi.error("File size must be less than 50MB");
				return Upload.LIST_IGNORE;
			}

			// ? Update parent component
			onFileChange(file);
			// ? Prevent default upload behavior
			return false;
		},
		onRemove: () => {
			onFileChange(null);
		},
		fileList: file ? [file] : [],
		showUploadList: {
			showPreviewIcon: false,
			showRemoveIcon: true,
			showDownloadIcon: false,
		},
	};

	return (
		<FlexContainer vertical gap={24}>
			{contextHolder}
			<Heading level={4}>Step 1: Upload a PDF File</Heading>

			<DraggerContainer {...uploadProps}>
				<InboxOutlined />
				<Heading level={5}>Click or drag PDF file to this area to upload</Heading>
				<SubHeading>
					Support for a single PDF file upload only. Files must be under 10MB in size.
				</SubHeading>
			</DraggerContainer>

			<Heading level={4}>Step 2: Enter password</Heading>
			<InputContainer>
				<Input.Password
					size="large"
					autoComplete="off"
					value={password ?? ""}
					id="pdf-password-input"
					prefix={<LockOutlined />}
					placeholder="Enter password"
					onChange={(e) => onPasswordChange(e.target.value)}
				/>
			</InputContainer>
		</FlexContainer>
	);
};

export { FileUpload };

const FlexContainer = styled(Flex)`
	text-align: center;

	padding: 1.5rem;
	max-width: 32rem;
	margin: 0 auto;
`;

const InputContainer = styled.div`
	padding: 1.25rem;
	border-radius: 0.5rem;
	min-height: 3.75rem;

	display: flex;
	align-items: center;
	justify-content: center;
`;

const Heading = styled(Title)`
	margin-bottom: 0.5rem;
	font-weight: 600;
`;

const SubHeading = styled(Text)`
	font-size: 0.5rem;
`;

const DraggerContainer = styled(Dragger)`
	border-radius: 0.5rem;

	transition: all 0.3s ease;

	.ant-upload {
		padding: 1rem 1.5rem;
	}

	.ant-upload-icon {
	}

	.anticon {
		font-size: 4rem;
	}
`;
