interface SegmentBarProps {
  height?: string;
}
export default function SegmentBar({ height }: SegmentBarProps) {
  return (
    <div className={`w-full ${height || 'h-2 md:h-4 lg:h-6'} flex overflow-hidden`}>
      {/* 1 */}
      <div className="flex-3 bg-foreground slice relative z-40"></div>

      {/* 2 */}
      <div className="flex-4 bg-secondary slice -ml-6 relative z-30"></div>

      {/* 3 */}
      <div className="flex-2 bg-[#BD31BB] slice -ml-6 relative z-20"></div>

      {/* 4 */}
      <div className="flex-1 bg-foreground -ml-6 relative z-10"></div>

    </div>
  );
}