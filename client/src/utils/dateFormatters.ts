/**
 * Formats a time label to display the day of the week with the date
 * Example: "Sat, Nov 2, 2024"
 */
export const formatTimeLabel = (timeLabel: string): string => {
  try {
    const date = new Date(timeLabel);
    const options: Intl.DateTimeFormatOptions = { 
      weekday: 'short', 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
  } catch {
    return timeLabel;
  }
};
