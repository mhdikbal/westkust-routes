import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import StorytellingOverlay from './StorytellingOverlay';

describe('StorytellingOverlay Component', () => {
  const mockTour = {
    title: "Test Tour",
    steps: [
      { yearSpan: [1700, 1720], title: "Step 1", content: "Content 1" },
      { yearSpan: [1721, 1750], title: "Step 2", content: "Content 2" }
    ]
  };

  test('does not render when tour is null', () => {
    const { container } = render(<StorytellingOverlay tour={null} stepIndex={0} />);
    expect(container).toBeEmptyDOMElement();
  });

  test('renders tour title and step content correctly', () => {
    render(<StorytellingOverlay tour={mockTour} stepIndex={0} />);
    
    expect(screen.getByText('Tur Sejarah: Test Tour')).toBeInTheDocument();
    expect(screen.getByText('Tahun 1700 - 1720')).toBeInTheDocument();
    expect(screen.getByText('Bab 1 dari 2')).toBeInTheDocument();
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('Content 1')).toBeInTheDocument();
  });

  test('disables prev button on first step', () => {
    render(<StorytellingOverlay tour={mockTour} stepIndex={0} onPrev={jest.fn()} onNext={jest.fn()} />);
    const prevBtn = screen.getByTestId('prev-step');
    expect(prevBtn).toBeDisabled();
  });

  test('calls onNext when Next is clicked', () => {
    const onNextMock = jest.fn();
    render(<StorytellingOverlay tour={mockTour} stepIndex={0} onNext={onNextMock} />);
    const nextBtn = screen.getByTestId('next-step');
    fireEvent.click(nextBtn);
    expect(onNextMock).toHaveBeenCalledTimes(1);
  });

  test('shows End Tour button on last step and calls onClose', () => {
    const onCloseMock = jest.fn();
    render(<StorytellingOverlay tour={mockTour} stepIndex={1} onClose={onCloseMock} />);
    const endBtn = screen.getByTestId('end-tour');
    expect(endBtn).toBeInTheDocument();
    
    // "Next" button should not be present
    expect(screen.queryByTestId('next-step')).not.toBeInTheDocument();
    
    fireEvent.click(endBtn);
    expect(onCloseMock).toHaveBeenCalledTimes(1);
  });
});
