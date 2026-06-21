import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { environment } from '../../../environments/environment';

interface Question {
    id: number;
    skill: string;
    question: string;
    answer: string;
    difficulty: string;
    topics: string[];
}

interface Resume {
    resume_id: string;
    data: {
        filename?: string;
        personal_info?: {
            name?: string;
            email?: string;
        };
        name?: string;
        skills: string[];
        email?: string;
    };
}

@Component({
    selector: 'app-skill-questions',
    standalone: true,
    imports: [CommonModule, HttpClientModule],
    templateUrl: './skill-questions.component.html',
    styleUrls: ['./skill-questions.component.css']
})
export class SkillQuestionsComponent implements OnInit {
    questions: Question[] = [];
    resumes: Resume[] = [];
    selectedResumeId: string = '';
    selectedResumeName: string = '';
    resumeSkills: string[] = [];
    loading = false;
    resumesLoading = false;
    error: string | null = null;
    showAnswers: boolean[] = [];

    get totalQuestions(): number {
        return this.questions.length;
    }

    get loadingResumes(): boolean {
        return this.resumesLoading;
    }

    get filteredQuestions(): Question[] {
        return this.questions;
    }

    filterByResume(resumeId: string | null) {
        if (resumeId) {
            this.selectResume(resumeId);
        } else {
            this.loadAllQuestions();
        }
    }

    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.loadResumes();
    }

    loadResumes() {
        this.resumesLoading = true;

        this.http.get<any>(`${this.apiUrl}/resumes?limit=50`).subscribe({
            next: (response) => {
                this.resumesLoading = false;
                this.resumes = response.resumes || [];

                // Auto-select first resume if available
                if (this.resumes.length > 0) {
                    this.selectResume(this.resumes[0].resume_id);
                }
            },
            error: (err) => {
                this.resumesLoading = false;
                console.error('Failed to load resumes:', err);
            }
        });
    }

    selectResume(resumeId: string) {
        this.selectedResumeId = resumeId;
        this.loadQuestionsForResume(resumeId);
    }

    loadQuestionsForResume(resumeId: string) {
        this.loading = true;
        this.error = null;

        this.http.get<any>(`${this.apiUrl}/resume/${resumeId}/skill-based-questions`).subscribe({
            next: (response) => {
                this.loading = false;
                this.questions = response.questions;
                this.selectedResumeName = response.candidate_name;
                this.resumeSkills = response.resume_skills || [];
                this.showAnswers = new Array(this.questions.length).fill(false);
            },
            error: (err) => {
                this.loading = false;
                this.error = err.error?.detail || 'Failed to load questions. Please try again.';
            }
        });
    }

    loadAllQuestions() {
        this.loading = true;
        this.error = null;
        this.selectedResumeId = '';
        this.selectedResumeName = '';
        this.resumeSkills = [];

        this.http.get<any>(`${this.apiUrl}/skill-questions`).subscribe({
            next: (response) => {
                this.loading = false;
                this.questions = response.questions;
                this.showAnswers = new Array(this.questions.length).fill(false);
            },
            error: (err) => {
                this.loading = false;
                this.error = err.error?.detail || 'Failed to load questions. Please try again.';
            }
        });
    }

    toggleAnswer(index: number) {
        this.showAnswers[index] = !this.showAnswers[index];
    }

    toggleAllAnswers() {
        const allShown = this.showAnswers.every(a => a);
        this.showAnswers = new Array(this.questions.length).fill(!allShown);
    }

    getSkillColor(skill: string): string {
        const colorMap: { [key: string]: string } = {
            'Python': '#3776AB',
            'JavaScript': '#F7DF1E',
            'React': '#61DAFB',
            'Node.js': '#339933',
            'SQL': '#336791',
            'API Design': '#FF6B6B',
            'Git': '#F05032',
            'Data Structures': '#6C5CE7',
            'Angular': '#DD0031',
            'Database': '#47A248',
            'Security': '#E74C3C',
            'System Design': '#9B59B6'
        };
        return colorMap[skill] || '#667eea';
    }

    getDifficultyClass(difficulty: string): string {
        return difficulty.toLowerCase();
    }

    getResumeName(resume: Resume): string {
        return resume.data.personal_info?.name || resume.data.name || resume.data.personal_info?.email || resume.data.email || 'Unknown';
    }
}
