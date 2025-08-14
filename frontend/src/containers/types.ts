type ActiveTab = "lock" | "unlock";

type Status = "idle" | "processing" | "processed" | "failed";

interface PasswordResponseData {
	message: string;
	filename: string;
	file_data: string;
}

export type { ActiveTab, Status, PasswordResponseData };
