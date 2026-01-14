#===================================================
# academic_report_writer.py
# Academic Report Content Generation System
# SAVE THIS AS: academic_report_writer.py (same directory as my_tools.py)
# Jan. 13, 2026
#===================================================

import json
from datetime import datetime
from typing import Dict, List, Any

def _safe_year(year_value, default=2020):
    """Safely convert year to integer"""
    if year_value is None:
        return default
    try:
        if isinstance(year_value, str):
            year_value = year_value.strip()
            if year_value.lower() in ['n/a', 'na', '', 'none']:
                return default
            return int(year_value)
        return int(year_value)
    except (ValueError, TypeError):
        return default

def _get_year_range(papers):
    """Get min and max years from paper list"""
    if not papers:
        return 2020, 2025
    years = [_safe_year(p.get('pub_year')) for p in papers]
    valid_years = [y for y in years if y is not None]
    if not valid_years:
        return 2020, 2025
    return min(valid_years), max(valid_years)

class AcademicReportWriter:
    """
    Automated academic report generation from research papers.
    Integrates with existing QuestScholar tools.
    """
    
    def __init__(self, collected_papers: List[Dict], critic_evaluations: Dict):
        self.papers = collected_papers
        self.evaluations = critic_evaluations
        self.report_data = {}
    
    def set_metadata(self, title: str, author: str, institution: str):
        """Set report metadata"""
        self.report_data['title'] = title
        self.report_data['author'] = author
        self.report_data['institution'] = institution
        self.report_data['date'] = datetime.now().strftime('%B %d, %Y')
    
    def generate_abstract(self, research_question: str, key_findings: str) -> str:
        """Generate abstract section (150-250 words)"""
        top_papers = [p for p in self.papers if p.get('critic_rank', 0) >= 4.0][:5]
        
        abstract = f"""This report presents a comprehensive analysis of research on {research_question}. 
A systematic review of {len(self.papers)} peer-reviewed publications from multiple academic databases 
was conducted, with {len(top_papers)} high-impact studies identified through rigorous quality assessment.

{key_findings}

The findings reveal significant advances in the field, with methodological innovations and emerging 
trends identified across {len(set(p.get('venue', 'Unknown') for p in self.papers))} distinct research venues. 
Papers published between {_get_year_range(self.papers)[0]} and {_get_year_range(self.papers)[1]} were analyzed, 
with particular emphasis on works demonstrating exceptional relevance and methodological rigor as determined 
by multi-criteria evaluation.

This report synthesizes key contributions, identifies research gaps, and provides evidence-based 
recommendations for future investigation."""
        
        self.report_data['abstract'] = abstract
        return abstract
    
    def generate_introduction(self, subject: str, context: str, objectives: List[str]) -> str:
        """Generate introduction section"""
        intro = f"""# 1. INTRODUCTION

## 1.1 Background and Context

{context}

The field of {subject} has experienced significant growth in recent years, as evidenced by 
the {len(self.papers)} scholarly publications analyzed in this report. These works span 
multiple research domains and methodological approaches, reflecting the interdisciplinary 
nature of contemporary inquiry.

## 1.2 Research Objectives

This report aims to:

"""
        for i, obj in enumerate(objectives, 1):
            intro += f"{i}. {obj}\n"
        
        intro += f"""
## 1.3 Scope and Limitations

This analysis encompasses peer-reviewed literature from four major academic databases: 
Semantic Scholar, PubMed, arXiv, and OpenAlex. Papers were selected based on relevance, 
methodological soundness, and research impact, with quality assessment performed using 
multi-criteria evaluation protocols.

The review focuses on publications from {_get_year_range(self.papers)[0]} to {_get_year_range(self.papers)[1]}, 
representing the most current research landscape.
"""
        
        self.report_data['introduction'] = intro
        return intro
    
    def generate_literature_review(self) -> str:
        """Generate literature review synthesizing top papers"""
        lit_review = "# 2. LITERATURE REVIEW\n\n"
        
        # Group by quality
        exceptional = [p for p in self.papers if p.get('critic_rank', 0) >= 4.5]
        excellent = [p for p in self.papers if 4.0 <= p.get('critic_rank', 0) < 4.5]
        
        lit_review += f"""## 2.1 Overview

The literature review identified {len(exceptional)} exceptional studies and {len(excellent)} 
excellent contributions warranting detailed analysis.

## 2.2 Key Research Contributions

"""
        
        # Top 10 papers
        top_papers = sorted(self.papers, key=lambda x: x.get('critic_rank', 0), reverse=True)[:10]
        
        for i, paper in enumerate(top_papers, 1):
            authors = ', '.join(paper.get('authors', ['Unknown'])[:3])
            if len(paper.get('authors', [])) > 3:
                authors += ' et al.'
            
            lit_review += f"""### 2.2.{i} {paper.get('title', 'Untitled')}

**Authors:** {authors} ({paper.get('pub_year', 'N/A')})  
**Source:** {paper.get('venue', 'Unknown')}  
**Quality Score:** {paper.get('critic_rank', 0):.2f}/5.0

{paper.get('abstract', 'No abstract available.')[:400]}...

"""
            
            # Add evaluation if available
            eval_key = paper.get('title', '').lower().strip()
            if eval_key in self.evaluations:
                lit_review += f"*Assessment: {self.evaluations[eval_key]['rationale']}*\n\n"
        
        self.report_data['literature_review'] = lit_review
        return lit_review
    
    def generate_methodology(self, search_params: Dict) -> str:
        """Generate methodology section"""
        methodology = f"""# 3. METHODOLOGY

## 3.1 Research Design

This study employed a systematic literature review methodology to identify, evaluate, and 
synthesize current research on the specified topic.

## 3.2 Data Collection

**Databases Searched:**
- Semantic Scholar (computer science and cross-disciplinary research)
- PubMed (biomedical and life sciences literature)
- arXiv (preprints and emerging research)
- OpenAlex (comprehensive open-access scholarly metadata)

**Search Parameters:**
- Keywords: {search_params.get('subject', 'N/A')}
- Date range: {search_params.get('start_year', 'N/A')} to {search_params.get('end_year', 'N/A')}
- Total papers retrieved: {len(self.papers)}

## 3.3 Quality Assessment

Papers were evaluated using multi-criteria assessment:
1. **Relevance** (0-5): Alignment with research objectives
2. **Methodological Soundness** (0-5): Research design quality
3. **Impact** (0-5): Citations and venue reputation

Papers scoring ≥4.0 were classified as high-quality ({len([p for p in self.papers if p.get('critic_rank', 0) >= 4.0])} papers).

## 3.4 Data Analysis

Papers were analyzed using thematic synthesis, citation analysis, and temporal trend identification.
"""
        
        self.report_data['methodology'] = methodology
        return methodology
    
    def generate_findings(self) -> str:
        """Generate findings with statistics"""
        findings = "# 4. FINDINGS\n\n## 4.1 Quantitative Analysis\n\n"
        
        findings += f"""| Metric | Value |
|--------|-------|
| Total Papers | {len(self.papers)} |
| Exceptional (≥4.5) | {len([p for p in self.papers if p.get('critic_rank', 0) >= 4.5])} |
| High Quality (≥4.0) | {len([p for p in self.papers if p.get('critic_rank', 0) >= 4.0])} |
| Year Range | {_get_year_range(self.papers)[0]}-{_get_year_range(self.papers)[1]} |
| Total Citations | {sum(p.get('citation_count', 0) for p in self.papers)} |

## 4.2 Key Findings

The analysis reveals several important patterns:

1. **Quality Distribution**: {len([p for p in self.papers if p.get('critic_rank', 0) >= 4.5])} papers achieved exceptional quality ratings
2. **Research Impact**: Top papers demonstrate significant citation influence
3. **Methodological Trends**: Increasing rigor in research design over time
4. **Publication Venues**: Diverse representation across {len(set(p.get('venue', 'Unknown') for p in self.papers))} venues
"""
        
        self.report_data['findings'] = findings
        return findings
    
    def generate_discussion(self, key_insights: List[str]) -> str:
        """Generate discussion interpreting findings"""
        discussion = f"""# 5. DISCUSSION

## 5.1 Interpretation of Findings

{key_insights[0] if key_insights else 'The analysis reveals important patterns across the literature.'}

The {len([p for p in self.papers if p.get('critic_rank', 0) >= 4.5])} exceptional papers 
represent the current research frontier, demonstrating innovative methodologies and significant contributions.

## 5.2 Research Trends

- Peak publication activity and increasing methodological sophistication
- Growing cross-disciplinary collaboration
- Enhanced focus on reproducibility and transparency

## 5.3 Implications

{key_insights[1] if len(key_insights) > 1 else 'These findings have significant implications for research and practice.'}

## 5.4 Research Gaps

Several areas require further investigation:
1. Longitudinal studies with larger sample sizes
2. Cross-cultural validation of findings
3. Integration of emerging technologies
4. Translation of research into practice
"""
        
        self.report_data['discussion'] = discussion
        return discussion
    
    def generate_conclusion(self, summary: str) -> str:
        """Generate conclusion"""
        conclusion = f"""# 6. CONCLUSION

This systematic review analyzed {len(self.papers)} peer-reviewed publications, identifying 
{len([p for p in self.papers if p.get('critic_rank', 0) >= 4.0])} high-quality contributions.

{summary}

The rigorous quality assessment ensures that highlighted contributions represent the most 
impactful and methodologically sound research currently available.
"""
        
        self.report_data['conclusion'] = conclusion
        return conclusion
    
    def generate_recommendations(self, recommendations: List[str]) -> str:
        """Generate recommendations"""
        rec = "# 7. RECOMMENDATIONS\n\nBased on the systematic review:\n\n"
        
        for i, recommendation in enumerate(recommendations, 1):
            rec += f"{i}. **{recommendation}**\n\n"
        
        self.report_data['recommendations'] = rec
        return rec
    
    def generate_references(self) -> str:
        """Generate formatted references"""
        refs = "# REFERENCES\n\n"
        
        sorted_papers = sorted(self.papers, 
                              key=lambda x: x.get('authors', ['ZZZ'])[0].split()[-1] if x.get('authors') else 'ZZZ')
        
        for i, paper in enumerate(sorted_papers, 1):
            authors = ', '.join(paper.get('authors', ['Unknown'])[:5])
            if len(paper.get('authors', [])) > 5:
                authors += ', et al.'
            
            refs += f"{i}. {authors} ({paper.get('pub_year', 'N/A')}). {paper.get('title', 'Untitled')}. "
            refs += f"*{paper.get('venue', 'Unknown')}*. {paper.get('source', 'Unknown')}. "
            refs += f"Available at: {paper.get('url', 'N/A')}\n\n"
        
        self.report_data['references'] = refs
        return refs
    
    def generate_full_report(self, params: Dict) -> Dict[str, str]:
        """Generate all sections"""
        self.generate_abstract(params['research_question'], params['key_findings'])
        self.generate_introduction(params['subject'], params['context'], params['objectives'])
        self.generate_literature_review()
        self.generate_methodology(params['search_params'])
        self.generate_findings()
        self.generate_discussion(params['key_insights'])
        self.generate_conclusion(params['summary'])
        self.generate_recommendations(params['recommendations'])
        self.generate_references()
        
        return self.report_data
    
    def export_to_markdown(self, filename: str = 'academic_report.md'):
        """Export to Markdown"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {self.report_data.get('title', 'Research Report')}\n\n")
            f.write(f"**Author:** {self.report_data.get('author', 'Unknown')}\n\n")
            f.write(f"**Institution:** {self.report_data.get('institution', 'Unknown')}\n\n")
            f.write(f"**Date:** {self.report_data.get('date', datetime.now().strftime('%B %d, %Y'))}\n\n")
            f.write("---\n\n")
            
            for section in ['abstract', 'introduction', 'literature_review', 
                          'methodology', 'findings', 'discussion', 
                          'conclusion', 'recommendations', 'references']:
                if self.report_data.get(section):
                    f.write(self.report_data[section])
                    f.write("\n\n")
        
        return f"✅ Markdown report exported: {filename}"


def generate_academic_report(collected_papers, critic_evaluations, report_params):
    """
    Main function to generate academic report
    Call this from your notebook after QuestScholar completes
    """
    writer = AcademicReportWriter(collected_papers, critic_evaluations)
    
    writer.set_metadata(
        title=report_params.get('title', 'Research Report'),
        author=report_params.get('author', 'Research Team'),
        institution=report_params.get('institution', 'Academic Institution')
    )
    
    report_data = writer.generate_full_report(report_params)
    
    md_file = report_params.get('output_file', 'academic_report.md')
    status = writer.export_to_markdown(md_file)
    
    return md_file, report_data