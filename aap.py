import React, { useState, useMemo } from 'react';
import { useApp } from '../context/AppContext';
import { COURSES_DATA } from '../data/coursesData';
import { QuizQuestion } from '../types';
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  Play,
  Pause,
  Volume2,
  Maximize2,
  FileText,
  Code2,
  HelpCircle,
  FolderArchive,
  ChevronDown,
  ChevronRight,
  ArrowRight,
  Copy,
  Check,
  RotateCcw
} from 'lucide-react';

export const CoursePlayer: React.FC = () => {
  const {
    selectedCourseId,
    selectedLessonId,
    setSelectedLessonId,
    setCurrentView,
    completedLessonIds,
    toggleLessonComplete,
    recordQuizAttempt,
    openPracticeProblem
  } = useApp();

  const course = useMemo(() => {
    return COURSES_DATA.find(c => c.id === selectedCourseId) || COURSES_DATA[0];
  }, [selectedCourseId]);

  // Find active lesson and active module
  const { currentLesson, currentModule, allLessons } = useMemo(() => {
    let foundLesson = null;
    let foundModule = null;
    const flatLessons: { lesson: any; module: any }[] = [];

    for (const mod of course.modules) {
      for (const les of mod.lessons) {
        flatLessons.push({ lesson: les, module: mod });
        if (les.id === selectedLessonId) {
          foundLesson = les;
          foundModule = mod;
        }
      }
    }

    if (!foundLesson && flatLessons.length > 0) {
      foundLesson = flatLessons[0].lesson;
      foundModule = flatLessons[0].module;
    }

    return { currentLesson: foundLesson, currentModule: foundModule, allLessons: flatLessons };
  }, [course, selectedLessonId]);

  const [activeTab, setActiveTab] = useState<'reading' | 'code' | 'quiz' | 'assignment'>('reading');
  
  // Video player simulator state
  const [isPlaying, setIsPlaying] = useState(false);
  const [videoProgress, setVideoProgress] = useState(24);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const [copiedCode, setCopiedCode] = useState(false);

  // Module quiz state
  const quiz = currentModule?.quiz;
  const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);

  // Lesson completion status
  const isLessonCompleted = currentLesson ? completedLessonIds.includes(currentLesson.id) : false;

  // Next / Previous navigation
  const currentIndex = allLessons.findIndex(item => item.lesson.id === currentLesson?.id);
  const prevLesson = currentIndex > 0 ? allLessons[currentIndex - 1].lesson : null;
  const nextLesson = currentIndex < allLessons.length - 1 ? allLessons[currentIndex + 1].lesson : null;

  // Course completion percentage
  const totalLessonsInCourse = allLessons.length;
  const completedInCourse = allLessons.filter(item => completedLessonIds.includes(item.lesson.id)).length;
  const completionPercentage = Math.round((completedInCourse / (totalLessonsInCourse || 1)) * 100);

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleQuizSubmit = () => {
    if (!quiz) return;
    setQuizSubmitted(true);

    let score = 0;
    quiz.questions.forEach((q: QuizQuestion) => {
      if (quizAnswers[q.id] === q.correctAnswerIndex) {
        score += 1;
      }
    });

    const percentage = Math.round((score / quiz.questions.length) * 100);
    recordQuizAttempt({
      quizId: quiz.id,
      quizTitle: quiz.title,
      score,
      totalQuestions: quiz.questions.length,
      percentage,
      passed: percentage >= quiz.passingScore,
      completedAt: 'Just now'
    });
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
      
      {/* Top Breadcrumb & Progress Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setCurrentView('courses')}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-100 dark:border-slate-800 dark:text-slate-300 dark:hover:bg-slate-800"
            title="Back to Course Catalog"
          >
            <ArrowLeft className="h-4 w-4" />
          </button>
          <div>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span>{course.category}</span>
              <span aria-hidden="true">·</span>
              <span>Level {course.levelNumber}</span>
            </div>
            <h1 className="text-lg font-bold text-slate-900 dark:text-white line-clamp-1">
              {course.title}
            </h1>
          </div>
        </div>

        {/* Course Progress indicator */}
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs font-semibold text-slate-900 dark:text-white">
              Course Progress: <span className="text-blue-600 dark:text-blue-400 tabular-nums">{completionPercentage}%</span>
            </div>
            <div className="text-[11px] text-slate-500 tabular-nums">
              {completedInCourse} of {totalLessonsInCourse} lessons completed
            </div>
          </div>
          <div className="h-2.5 w-24 sm:w-32 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
            <div
              className="h-full bg-blue-600 transition-all duration-300"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Main 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Lesson Content, Video & Tabs (8 cols) */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Simulated Video Player Stage */}
          <div className="relative rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 shadow-xl group">
            {/* Visual Screen */}
            <div className="relative h-64 sm:h-96 w-full flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 p-6 text-center select-none">
              
              <div className="space-y-3 max-w-lg z-10">
                <span className="inline-block rounded-md bg-blue-500/20 px-2.5 py-1 text-xs font-mono font-semibold text-blue-400 border border-blue-400/30">
                  {currentModule?.title}
                </span>
                <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                  {currentLesson?.title}
                </h3>
                <p className="text-xs text-slate-400">
                  Interactive Academic Lecture · Instructor: {course.instructor.name}
                </p>
                
                {/* Simulated center play button */}
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg hover:scale-110 hover:bg-blue-500 transition-transform mt-4"
                  aria-label={isPlaying ? 'Pause video' : 'Play video'}
                >
                  {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6 ml-1" />}
                </button>
              </div>

              {/* Watermark grid effect */}
              <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:16px_16px]" />
            </div>

            {/* Video Controls Bar */}
            <div className="border-t border-slate-800 bg-slate-900/90 backdrop-blur-md px-4 py-3 flex items-center justify-between text-xs text-slate-300">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="text-white hover:text-blue-400 transition-colors"
                >
                  {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </button>
                <div className="flex items-center gap-1.5 font-mono text-[11px] tabular-nums text-slate-400">
                  <span>04:12</span>
                  <span>/</span>
                  <span>{currentLesson?.duration || '15:00'}</span>
                </div>
              </div>

              {/* Video scrubber */}
              <div className="flex-1 mx-4">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={videoProgress}
                  onChange={e => setVideoProgress(Number(e.target.value))}
                  className="w-full accent-blue-500 cursor-pointer h-1 rounded bg-slate-700"
                />
              </div>

              <div className="flex items-center gap-3">
                {/* Playback speed toggle */}
                <button
                  onClick={() => {
                    const speeds = [1.0, 1.25, 1.5, 2.0];
                    const next = speeds[(speeds.indexOf(playbackSpeed) + 1) % speeds.length];
                    setPlaybackSpeed(next);
                  }}
                  className="font-mono text-[11px] px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
                >
                  {playbackSpeed}x
                </button>
                <Volume2 className="h-4 w-4 text-slate-400 hover:text-white cursor-pointer" />
                <Maximize2 className="h-4 w-4 text-slate-400 hover:text-white cursor-pointer" />
              </div>
            </div>
          </div>

          {/* Lesson Tab Controls */}
          <div className="flex items-center border-b border-slate-200 dark:border-slate-800 gap-2">
            <button
              onClick={() => setActiveTab('reading')}
              className={`flex items-center gap-2 py-3 px-3 text-xs font-semibold border-b-2 transition-colors ${
                activeTab === 'reading'
                  ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
                  : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
              }`}
            >
              <FileText className="h-4 w-4" />
              <span>Lecture Notes & Reading</span>
            </button>

            {currentLesson?.codeSnippet && (
              <button
                onClick={() => setActiveTab('code')}
                className={`flex items-center gap-2 py-3 px-3 text-xs font-semibold border-b-2 transition-colors ${
                  activeTab === 'code'
                    ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
                    : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
                }`}
              >
                <Code2 className="h-4 w-4" />
                <span>Code Example</span>
              </button>
            )}

            {quiz && (
              <button
                onClick={() => setActiveTab('quiz')}
                className={`flex items-center gap-2 py-3 px-3 text-xs font-semibold border-b-2 transition-colors ${
                  activeTab === 'quiz'
                    ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
                    : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
                }`}
              >
                <HelpCircle className="h-4 w-4" />
                <span>Module Quiz</span>
              </button>
            )}

            <button
              onClick={() => setActiveTab('assignment')}
              className={`flex items-center gap-2 py-3 px-3 text-xs font-semibold border-b-2 transition-colors ${
                activeTab === 'assignment'
                  ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
                  : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'
              }`}
            >
              <FolderArchive className="h-4 w-4" />
              <span>Assignment</span>
            </button>
          </div>

          {/* Tab 1: Reading Material */}
          {activeTab === 'reading' && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900 space-y-6">
              <div className="prose dark:prose-invert max-w-none text-sm text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line">
                {currentLesson?.content}
              </div>

              {/* Key Takeaways Box */}
              {currentLesson?.keyTakeaways && currentLesson.keyTakeaways.length > 0 && (
                <div className="rounded-xl border border-blue-200/80 bg-blue-50/60 p-5 dark:border-blue-900/40 dark:bg-blue-950/30">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900 dark:text-blue-300 mb-3">
                    Key Academic Takeaways
                  </h4>
                  <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
                    {currentLesson.keyTakeaways.map((takeaway: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2">
                        <CheckCircle2 className="h-4 w-4 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
                        <span>{takeaway}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Tab 2: Code Example */}
          {activeTab === 'code' && currentLesson?.codeSnippet && (
            <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden dark:border-slate-800 dark:bg-slate-900 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 bg-slate-100 px-4 py-2.5 dark:border-slate-800 dark:bg-slate-950">
                <span className="font-mono text-xs text-slate-600 dark:text-slate-400">
                  {currentLesson.codeSnippet.language.toUpperCase()} Snippet
                </span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleCopyCode(currentLesson.codeSnippet!.code)}
                    className="flex items-center gap-1.5 rounded bg-white px-2.5 py-1 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                  >
                    {copiedCode ? <Check className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copiedCode ? 'Copied!' : 'Copy Code'}</span>
                  </button>
                  <button
                    onClick={() => openPracticeProblem('prob-py-1')}
                    className="flex items-center gap-1 rounded bg-blue-600 px-2.5 py-1 text-xs font-semibold text-white hover:bg-blue-700"
                  >
                    <span>Run in Sandbox</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>

              <div className="p-4">
                <pre className="rounded-xl bg-slate-950 p-4 font-mono text-xs text-slate-200 overflow-x-auto leading-relaxed">
                  {currentLesson.codeSnippet.code}
                </pre>
                <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">
                  <strong className="text-slate-700 dark:text-slate-200">Explanation: </strong>
                  {currentLesson.codeSnippet.explanation}
                </p>
              </div>
            </div>
          )}

          {/* Tab 3: Interactive Module Quiz */}
          {activeTab === 'quiz' && quiz && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900 space-y-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                  {quiz.title}
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  {quiz.description} (Passing score: {quiz.passingScore}%)
                </p>
              </div>

              <div className="space-y-6">
                {quiz.questions.map((q: QuizQuestion, qIndex: number) => {
                  const selectedAnswer = quizAnswers[q.id];
                  const isCorrect = selectedAnswer === q.correctAnswerIndex;
                  return (
                    <div
                      key={q.id}
                      className="rounded-xl border border-slate-200 p-4 dark:border-slate-800 space-y-3"
                    >
                      <p className="text-sm font-semibold text-slate-900 dark:text-white">
                        {qIndex + 1}. {q.question}
                      </p>

                      <div className="space-y-2">
                        {q.options.map((option: string, optIndex: number) => {
                          const isOptSelected = selectedAnswer === optIndex;
                          let optStyle = 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60';
                          
                          if (quizSubmitted) {
                            if (optIndex === q.correctAnswerIndex) {
                              optStyle = 'border-emerald-500 bg-emerald-50 text-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300';
                            } else if (isOptSelected) {
                              optStyle = 'border-red-500 bg-red-50 text-red-900 dark:bg-red-950/40 dark:text-red-300';
                            }
                          } else if (isOptSelected) {
                            optStyle = 'border-blue-500 bg-blue-50 text-blue-900 dark:bg-blue-950/50 dark:text-blue-300 ring-1 ring-blue-500';
                          }

                          return (
                            <button
                              key={optIndex}
                              onClick={() => {
                                if (!quizSubmitted) {
                                  setQuizAnswers(prev => ({ ...prev, [q.id]: optIndex }));
                                }
                              }}
                              className={`w-full text-left p-3 rounded-lg border text-xs font-medium transition-colors ${optStyle}`}
                            >
                              <span>{option}</span>
                            </button>
                          );
                        })}
                      </div>

                      {quizSubmitted && (
                        <div className={`mt-2 p-3 rounded-lg text-xs leading-relaxed ${
                          isCorrect
                            ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border border-emerald-200/60'
                            : 'bg-red-50 text-red-800 dark:bg-red-950/40 dark:text-red-300 border border-red-200/60'
                        }`}>
                          <strong className="block mb-0.5">
                            {isCorrect ? '✔ Correct Answer' : '✘ Incorrect Answer'}
                          </strong>
                          {q.explanation}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Submit / Retake button */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-800">
                {!quizSubmitted ? (
                  <button
                    onClick={handleQuizSubmit}
                    disabled={Object.keys(quizAnswers).length < quiz.questions.length}
                    className="px-5 py-2.5 text-xs font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm transition-colors"
                  >
                    Submit Quiz Answers
                  </button>
                ) : (
                  <div className="flex items-center justify-between w-full">
                    <span className="text-xs font-bold text-slate-900 dark:text-white">
                      Your Score: {quiz.questions.filter((q: QuizQuestion) => quizAnswers[q.id] === q.correctAnswerIndex).length}/{quiz.questions.length}
                    </span>
                    <button
                      onClick={() => {
                        setQuizSubmitted(false);
                        setQuizAnswers({});
                      }}
                      className="flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-700 dark:text-blue-400"
                    >
                      <RotateCcw className="h-3.5 w-3.5" />
                      <span>Retake Quiz</span>
                    </button>
                  </div>
                )}
              </div>

            </div>
          )}

          {/* Tab 4: Assignment */}
          {activeTab === 'assignment' && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Practical Module Assignment
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                Apply the concepts explored in this module by completing a hands-on problem on your local machine or inside the PRP ScholarHub Practice Zone.
              </p>
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950 text-xs space-y-2">
                <p className="font-semibold text-slate-800 dark:text-slate-200">Assignment Objectives:</p>
                <ol className="list-decimal pl-4 space-y-1 text-slate-600 dark:text-slate-400">
                  <li>Implement the core function described in today's lecture.</li>
                  <li>Verify behavior on edge cases: empty collections, single element inputs, and extreme outliers.</li>
                  <li>Benchmark execution time and memory footprint against baseline implementations.</li>
                </ol>
              </div>

              <div className="pt-2">
                <button
                  onClick={() => openPracticeProblem('prob-py-1')}
                  className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700"
                >
                  <span>Open Coding Sandbox</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {/* Bottom Lesson Navigation Bar */}
          <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-slate-200 dark:border-slate-800">
            {prevLesson ? (
              <button
                onClick={() => setSelectedLessonId(prevLesson.id)}
                className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
              >
                <ArrowLeft className="h-3.5 w-3.5" />
                <span>Previous: {prevLesson.title.slice(0, 24)}...</span>
              </button>
            ) : <div />}

            <button
              onClick={() => currentLesson && toggleLessonComplete(currentLesson.id)}
              className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg shadow-sm transition-colors ${
                isLessonCompleted
                  ? 'bg-emerald-600 text-white hover:bg-emerald-700'
                  : 'bg-slate-900 text-white hover:bg-slate-800 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-100'
              }`}
            >
              <CheckCircle2 className="h-4 w-4" />
              <span>{isLessonCompleted ? 'Lesson Completed' : 'Mark as Complete'}</span>
            </button>

            {nextLesson ? (
              <button
                onClick={() => setSelectedLessonId(nextLesson.id)}
                className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 shadow-sm"
              >
                <span>Next: {nextLesson.title.slice(0, 24)}...</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            ) : <div />}
          </div>

        </div>

        {/* Right Column: Course Curriculum Accordion (4 cols) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-3">
              Course Syllabus
            </h3>

            <div className="space-y-3">
              {course.modules.map(module => (
                <div
                  key={module.id}
                  className="rounded-xl border border-slate-100 bg-slate-50 dark:border-slate-800 dark:bg-slate-950/60 overflow-hidden"
                >
                  <div className="p-3 bg-slate-100/70 dark:bg-slate-800/50">
                    <p className="text-xs font-bold text-slate-900 dark:text-white">
                      {module.title}
                    </p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      {module.lessons.length} lessons · {module.duration}
                    </p>
                  </div>

                  <div className="divide-y divide-slate-100 dark:divide-slate-800/60">
                    {module.lessons.map(lesson => {
                      const isCurrent = lesson.id === currentLesson?.id;
                      const isDone = completedLessonIds.includes(lesson.id);
                      return (
                        <button
                          key={lesson.id}
                          onClick={() => setSelectedLessonId(lesson.id)}
                          className={`flex items-start gap-2.5 w-full p-2.5 text-left text-xs transition-colors ${
                            isCurrent
                              ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 font-semibold'
                              : 'text-slate-700 hover:bg-slate-100/80 dark:text-slate-300 dark:hover:bg-slate-800/40'
                          }`}
                        >
                          {isDone ? (
                            <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                          ) : (
                            <Circle className="h-4 w-4 text-slate-300 dark:text-slate-600 shrink-0 mt-0.5" />
                          )}
                          <div className="min-w-0">
                            <p className="truncate">{lesson.title}</p>
                            <span className="text-[10px] text-slate-400 font-mono">
                              {lesson.duration} · {lesson.type}
                            </span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

          </div>
        </div>

      </div>

    </div>
  );
};
