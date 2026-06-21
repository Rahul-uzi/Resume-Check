import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeService } from '../../services/resume.service';

interface Question {
    id: number;
    skill: string;
    question: string;
    answer: string;
    difficulty: string;
    topics: string[];
}

@Component({
    selector: 'app-questions',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './questions.component.html',
    styleUrls: ['./questions.component.css']
})
export class QuestionsComponent implements OnInit {
    @Input() resumeId: string = '';

    questions: Question[] = [];
    loading = false;
    error: string | null = null;
    showAnswers: boolean[] = [];

    constructor(private resumeService: ResumeService) { }

    ngOnInit() {
        if (this.resumeId) {
            this.loadQuestions();
        }
    }

    loadQuestions() {
        this.loading = true;
        this.error = null;

        this.resumeService.getInterviewQuestions(this.resumeId).subscribe({
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

    getSkillColor(index: number): string {
        const colors = [
            '#667eea', '#764ba2', '#f093fb', '#4facfe',
            '#43e97b', '#fa709a', '#fee140', '#30cfd0'
        ];
        return colors[index % colors.length];
    }
}
