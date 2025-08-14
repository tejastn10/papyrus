import { FC } from "react";

import { Button } from "antd";
import { SyncOutlined } from "@ant-design/icons";

import { Status } from "../containers/types";

interface Props {
	status: Status;
	retry: () => void;
	process: () => void;
	download: () => void;
}

const FileDownload: FC<Props> = ({ status, retry, process, download }) => {
	const onClick = () => {
		switch (status) {
			case "failed":
				retry();
				break;
			case "idle":
			case "processing":
				process();
				break;
			case "processed":
				download();
				break;
			default:
				break;
		}
	};

	const getButtonText = () => {
		switch (status) {
			case "failed":
				return "Retry";
			case "processing":
				return "Processing";
			case "processed":
				return "Download";
			case "idle":
			default:
				return "Process";
		}
	};

	return (
		<>
			<Button
				size="large"
				onClick={onClick}
				className="process"
				disabled={status === "processing"}
				icon={<SyncOutlined spin={status === "processing"} />}
			>
				{getButtonText()}
			</Button>
		</>
	);
};

export { FileDownload };
