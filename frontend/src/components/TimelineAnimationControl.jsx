import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Play, Pause, RotateCcw } from "lucide-react";

export default function TimelineAnimationControl({ yearRange, setYearRange, minYear, maxYear }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentYear, setCurrentYear] = useState(minYear);
  const [speed, setSpeed] = useState(1); // Years per second
  const intervalRef = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentYear((prev) => {
          if (prev >= maxYear) {
            setIsPlaying(false);
            return maxYear;
          }
          return prev + 1;
        });
      }, 1000 / speed);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isPlaying, speed, maxYear]);

  useEffect(() => {
    setYearRange([minYear, currentYear]);
  }, [currentYear, minYear, setYearRange]);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setIsPlaying(false);
    setCurrentYear(minYear);
    setYearRange([minYear, minYear + 10]);
  };

  const handleSpeedChange = (newSpeed) => {
    setSpeed(newSpeed[0]);
  };

  return (
    <div className="absolute bottom-6 right-6 bg-[#FDFBF7]/95 backdrop-blur-xl rounded-lg border-2 border-[#E6E2D6] shadow-[0_8px_32px_rgba(26,36,33,0.12)] p-5 w-80">
      <div className="space-y-4">
        {/* Title */}
        <div className="flex items-center justify-between">
          <h3 className="font-serif text-lg font-bold text-[#1A2421]">
            Timeline Animation
          </h3>
          <div className="text-2xl font-serif font-bold text-[#B85D19]">
            {currentYear}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative">
          <div className="h-2 bg-[#E6E2D6] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#B85D19] to-[#D4AF37] transition-all duration-300"
              style={{
                width: `${((currentYear - minYear) / (maxYear - minYear)) * 100}%`,
              }}
            />
          </div>
          <div className="flex justify-between mt-1 text-xs text-[#8A9A95]">
            <span>{minYear}</span>
            <span>{maxYear}</span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-2">
          <Button
            onClick={handlePlayPause}
            size="sm"
            className="bg-[#B85D19] hover:bg-[#9a4d15] text-white flex-1"
            data-testid="timeline-play-pause"
          >
            {isPlaying ? (
              <>
                <Pause className="w-4 h-4 mr-2" />
                Pause
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Play
              </>
            )}
          </Button>
          <Button
            onClick={handleReset}
            size="sm"
            variant="outline"
            className="border-[#E6E2D6] hover:bg-[#FDFBF7]"
            data-testid="timeline-reset"
          >
            <RotateCcw className="w-4 h-4" />
          </Button>
        </div>

        {/* Speed Control */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-[#5C6A66]">Kecepatan</span>
            <span className="text-sm font-medium text-[#1A2421]">{speed}x</span>
          </div>
          <Slider
            value={[speed]}
            onValueChange={handleSpeedChange}
            min={0.5}
            max={5}
            step={0.5}
            className="w-full"
          />
        </div>

        {/* Info */}
        <div className="text-xs text-[#8A9A95] italic text-center">
          Animasi menampilkan pelayaran dari {minYear} hingga tahun yang dipilih
        </div>
      </div>
    </div>
  );
}
