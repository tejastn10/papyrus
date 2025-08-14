import { RcFile } from "antd/es/upload";

export const isPdfFile = (file: RcFile) => {
	return file && file.type === "application/pdf";
};

export const isValidFileSize = (file: RcFile) => {
	const maxSize = 50 * 1024 * 1024; // 50MB in bytes
	return file && file.size <= maxSize;
};
