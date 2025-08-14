import { RcFile } from "antd/es/upload";

import { POST, URLVersions } from "../api/helper";

import { ContentType } from "../config/requestConfig";
import { logError } from "../log/logger";

const SLUG = "password";

const lock = async ({ file, password }: { file: RcFile; password: string }) => {
	const formData = new FormData();
	formData.append("file", file);
	formData.append("password", password);

	const response = POST({
		url: `${SLUG}/lock`,
		version: URLVersions.V1,
		data: formData,
		apiConfig: {
			headers: {
				"Content-Type": ContentType.FORM_DATA,
			},
		},
	});

	return response;
};

const unlock = async ({ file, password }: { file: RcFile; password: string }) => {
	const formData = new FormData();
	formData.append("file", file);
	formData.append("password", password);

	const response = POST({
		url: `${SLUG}/unlock`,
		version: URLVersions.V1,
		data: formData,
		apiConfig: {
			headers: {
				"Content-Type": ContentType.FORM_DATA,
			},
		},
	});

	return response;
};

const download = ({ file_data, filename }: { file_data: string; filename: string }) => {
	try {
		// Convert base64 to blob
		const byteCharacters = atob(file_data);
		const byteNumbers = new Array(byteCharacters.length);

		for (let i = 0; i < byteCharacters.length; i++) {
			byteNumbers[i] = byteCharacters.charCodeAt(i);
		}

		const byteArray = new Uint8Array(byteNumbers);
		const blob = new Blob([byteArray], { type: "application/pdf" });

		// Create download link
		const url = window.URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = url;
		link.download = filename;

		// Trigger download
		document.body.appendChild(link);
		link.click();

		// Cleanup
		document.body.removeChild(link);
		window.URL.revokeObjectURL(url);
	} catch (error) {
		logError(`Error downloading file: ${JSON.stringify(error, null, 2)}`);
		throw new Error("Failed to download file");
	}
};

export { lock, unlock, download };
