/**
 * Truncates a long message to a specified length
 * @param text Message text to truncate
 * @param maxLength Maximum allowed length
 * @returns Truncated text with ellipsis if needed
 */
export const truncateMessage = (text: string, maxLength: number = 100): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Formats a timestamp into a human-readable time string
 * @param date Date object or ISO string
 * @returns Formatted time string
 */
export const formatMessageTime = (date: Date | string): string => {
  const messageDate = typeof date === 'string' ? new Date(date) : date;
  return messageDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

/**
 * Formats a timestamp into a date string if the message is from a different day
 * @param date Date object or ISO string
 * @returns Formatted date string or empty string if today
 */
export const formatMessageDate = (date: Date | string): string => {
  const messageDate = typeof date === 'string' ? new Date(date) : date;
  const today = new Date();
  
  if (
    messageDate.getDate() === today.getDate() &&
    messageDate.getMonth() === today.getMonth() &&
    messageDate.getFullYear() === today.getFullYear()
  ) {
    return '';
  }
  
  return messageDate.toLocaleDateString();
};

/**
 * Escapes HTML in a message to prevent XSS
 * @param text Raw message text
 * @returns Escaped HTML string
 */
export const escapeHTML = (text: string): string => {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
};