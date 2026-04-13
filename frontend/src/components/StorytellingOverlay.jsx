import React from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, X, Compass } from "lucide-react";

export default function StorytellingOverlay({
  tour,
  stepIndex,
  onNext,
  onPrev,
  onClose,
}) {
  if (!tour || !tour.steps || tour.steps.length === 0) return null;

  const currentStep = tour.steps[stepIndex];
  const isFirst = stepIndex === 0;
  const isLast = stepIndex === tour.steps.length - 1;

  return (
    <Card 
      className="absolute bottom-8 left-8 w-[400px] z-[50] bg-[#0A0E1A]/95 border-b-4 border-b-[#D4AF37] border-t-white/10 border-l-white/10 border-r-white/10 backdrop-blur-md shadow-2xl p-0 overflow-hidden flex flex-col pointer-events-auto"
      data-testid="storytelling-overlay"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10 bg-gradient-to-r from-[#D4AF37]/10 to-transparent">
        <div className="flex items-center gap-2">
          <Compass className="w-5 h-5 text-[#D4AF37]" />
          <h3 className="font-serif font-bold text-white text-sm">
            Tur Sejarah: {tour.title}
          </h3>
        </div>
        <button
          onClick={onClose}
          className="text-white/50 hover:text-white transition-colors"
          data-testid="close-tour"
        >
          <X className="w-4 h-4 cursor-pointer" />
        </button>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1 bg-[#D4AF37]/20 flex">
        {tour.steps.map((_, idx) => (
          <div
            key={idx}
            className={`flex-1 h-full transition-all duration-500 border-r border-[#0A0E1A] last:border-r-0 ${
              idx <= stepIndex ? "bg-[#D4AF37]" : "bg-transparent"
            }`}
          />
        ))}
      </div>

      {/* Content */}
      <div className="p-6 flex-1 min-h-[160px]">
        <div className="flex flex-col h-full justify-center">
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-mono text-[#00D4AA] tracking-wider uppercase">
              Tahun {currentStep.yearSpan[0]} - {currentStep.yearSpan[1]}
            </span>
            <span className="text-xs text-white/40">
              Bab {stepIndex + 1} dari {tour.steps.length}
            </span>
          </div>
          
          <h2 className="text-xl font-bold font-serif text-white mb-3">
            {currentStep.title}
          </h2>
          
          <p className="text-sm text-white/70 leading-relaxed">
            {currentStep.content}
          </p>
        </div>
      </div>

      {/* Footer Nav */}
      <div className="p-4 border-t border-white/10 flex items-center justify-between bg-white/5">
        <Button
          variant="outline"
          size="sm"
          className="border-white/10 hover:bg-white/10 bg-transparent text-white"
          onClick={onPrev}
          disabled={isFirst}
          data-testid="prev-step"
        >
          <ChevronLeft className="w-4 h-4 mr-1" />
          Kilas Balik
        </Button>

        {isLast ? (
          <Button
            size="sm"
            className="bg-[#D4AF37] hover:bg-[#B3932E] text-black font-semibold"
            onClick={onClose}
            data-testid="end-tour"
          >
            Selesai Tur
          </Button>
        ) : (
          <Button
            size="sm"
            className="bg-[#D4AF37] hover:bg-[#B3932E] text-black font-semibold"
            onClick={onNext}
            data-testid="next-step"
          >
            Lanjutkan
            <ChevronRight className="w-4 h-4 ml-1" />
          </Button>
        )}
      </div>
    </Card>
  );
}
