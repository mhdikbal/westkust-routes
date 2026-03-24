import { Slider } from "@/components/ui/slider";
import { Calendar, Play } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TimelineSlider({ yearRange, setYearRange, minYear, maxYear, onToggleAnimation, showAnimation }) {
  return (
    <div
      className="absolute bottom-6 left-[27rem] right-6 bg-[#FDFBF7]/90 backdrop-blur-xl rounded-lg border border-[#E6E2D6] shadow-[0_8px_32px_rgba(26,36,33,0.08)] p-6"
      data-testid="timeline-slider"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Calendar className="w-5 h-5 text-[#B85D19]" />
          <h3 className="font-serif text-lg font-semibold text-[#1A2421]">
            Timeline Pelayaran
          </h3>
        </div>
        <div className="flex items-center gap-4">
          <Button
            onClick={onToggleAnimation}
            size="sm"
            variant={showAnimation ? "default" : "outline"}
            className={showAnimation ? "bg-[#B85D19] hover:bg-[#9a4d15]" : "border-[#E6E2D6]"}
          >
            <Play className="w-4 h-4 mr-1" />
            {showAnimation ? "Mode Animasi" : "Animasi"}
          </Button>
          <span className="text-sm font-medium text-[#5C6A66]">
            {yearRange[0]} - {yearRange[1]}
          </span>
        </div>
      </div>

      <Slider
        value={yearRange}
        onValueChange={setYearRange}
        min={minYear}
        max={maxYear}
        step={1}
        className="w-full"
        data-testid="year-range-slider"
      />

      <div className="flex justify-between mt-2 text-xs text-[#8A9A95]">
        <span>{minYear}</span>
        <span>{maxYear}</span>
      </div>
    </div>
  );
}