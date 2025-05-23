/**
 * Validates if the file is of an allowed type
 * @param file File to validate
 * @returns boolean indicating if the file is valid
 */
export const isValidFileType = (file: File): boolean => {
  const validTypes = [
    'application/pdf', 
    'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
    'text/plain'
  ];
  return validTypes.includes(file.type);
};

/**
 * Formats file size in human-readable format
 * @param bytes Size in bytes
 * @returns Formatted string (e.g., "2.5 MB")
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' bytes';
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  else return (bytes / 1048576).toFixed(1) + ' MB';
};

/**
 * Checks if the file extension matches one of the allowed extensions
 * @param fileName Name of the file
 * @returns boolean indicating if the file extension is valid
 */
export const hasValidExtension = (fileName: string): boolean => {
  const validExtensions = ['.pdf', '.doc', '.docx', '.txt'];
  const extension = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();
  return validExtensions.includes(extension);
};

/**
 * Generates a unique ID for a file
 * @returns A unique string ID
 */
export const generateFileId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
};