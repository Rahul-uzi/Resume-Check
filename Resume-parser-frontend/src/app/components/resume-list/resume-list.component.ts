import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeService, ParsedResume } from '../../services/resume.service';
import { QuestionsComponent } from '../questions/questions.component';

@Component({
    selector: 'app-resume-list',
    standalone: true,
    imports: [CommonModule, QuestionsComponent],
    templateUrl: './resume-list.component.html',
    styleUrls: ['./resume-list.component.css']
})
export class ResumeListComponent implements OnInit {
    resumes: any[] = [];
    loading = false;
    error: string | null = null;
    total = 0;
    currentPage = 0;
    pageSize = 10;
    selectedResume: any = null;
    Math = Math; // Make Math available in template
    showQuestions = false;
    questionsResumeId: string = '';
    showDeleteConfirm = false;
    resumeToDeleteId: string = '';
    isDeleting = false;

    constructor(private resumeService: ResumeService) { }

    ngOnInit() {
        this.loadResumes();
    }

    loadResumes() {
        this.loading = true;
        this.error = null;

        this.resumeService.getAllResumes(this.currentPage * this.pageSize, this.pageSize).subscribe({
            next: (response) => {
                this.loading = false;
                this.resumes = response.resumes;
                this.total = response.total;
            },
            error: (err) => {
                this.loading = false;
                this.error = 'Failed to load resumes. Please try again.';
            }
        });
    }

    viewResume(resume: any) {
        this.selectedResume = resume;
        this.showQuestions = false;
    }

    viewQuestions(resumeId: string, event: Event) {
        event.stopPropagation();
        this.questionsResumeId = resumeId;
        this.showQuestions = true;
        this.selectedResume = null;
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.selectedResume = null;
        this.showQuestions = false;
        this.showDeleteConfirm = false;
        document.body.style.overflow = 'auto';
    }

    deleteResume(resumeId: string, event: Event) {
        event.stopPropagation();
        this.resumeToDeleteId = resumeId;
        this.showDeleteConfirm = true;
        document.body.style.overflow = 'hidden';
    }

    cancelDelete() {
        this.showDeleteConfirm = false;
        this.resumeToDeleteId = '';
        document.body.style.overflow = 'auto';
    }

    confirmDelete() {
        if (!this.resumeToDeleteId) return;

        this.isDeleting = true;
        this.resumeService.deleteResume(this.resumeToDeleteId).subscribe({
            next: () => {
                this.isDeleting = false;
                this.showDeleteConfirm = false;
                this.resumeToDeleteId = '';
                document.body.style.overflow = 'auto';
                this.loadResumes();
            },
            error: (err) => {
                this.isDeleting = false;
                this.showDeleteConfirm = false;
                document.body.style.overflow = 'auto';
                this.error = 'Failed to delete resume. Please try again.';
            }
        });
    }

    nextPage() {
        if ((this.currentPage + 1) * this.pageSize < this.total) {
            this.currentPage++;
            this.loadResumes();
        }
    }

    previousPage() {
        if (this.currentPage > 0) {
            this.currentPage--;
            this.loadResumes();
        }
    }
}
