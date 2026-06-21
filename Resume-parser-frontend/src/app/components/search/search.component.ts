import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ResumeService, SearchRequest, SearchResult } from '../../services/resume.service';
import { QuestionsComponent } from '../questions/questions.component';

@Component({
    selector: 'app-search',
    standalone: true,
    imports: [CommonModule, FormsModule, QuestionsComponent],
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})
export class SearchComponent {
    searchQuery = '';
    minExperience: number | null = null;
    skills: string = '';
    loading = false;
    searchResults: SearchResult[] = [];
    error: string | null = null;
    selectedResume: any = null;
    showQuestions = false;
    questionsResumeId: string = '';

    constructor(private resumeService: ResumeService) { }

    search() {
        if (!this.searchQuery.trim()) {
            this.error = 'Please enter a search query';
            return;
        }

        this.loading = true;
        this.error = null;
        this.searchResults = [];

        const request: SearchRequest = {
            query: this.searchQuery,
            filters: {},
            limit: 20
        };

        if (this.minExperience !== null && this.minExperience > 0) {
            request.filters!['min_experience'] = this.minExperience;
        }

        if (this.skills.trim()) {
            request.filters!['skills'] = this.skills.split(',').map(s => s.trim());
        }

        this.resumeService.searchResumes(request).subscribe({
            next: (response) => {
                this.loading = false;
                this.searchResults = response.results;
            },
            error: (err) => {
                this.loading = false;
                this.error = 'Search failed. Please try again.';
            }
        });
    }

    viewResume(result: SearchResult) {
        this.selectedResume = { resume_id: result.resume_id, data: result.data, score: result.score };
    }

    closeModal() {
        this.selectedResume = null;
        this.showQuestions = false;
    }

    clearSearch() {
        this.searchQuery = '';
        this.minExperience = null;
        this.skills = '';
        this.searchResults = [];
        this.error = null;
    }
}
