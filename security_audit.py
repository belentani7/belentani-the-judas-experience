#!/usr/bin/env python3
"""
Security Audit Script for Belentani Judas Experience
Performs automated security checks and generates audit reports
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class SecurityAuditor:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = []
        self.severity_levels = {
            'CRITICAL': 4,
            'HIGH': 3,
            'MEDIUM': 2,
            'LOW': 1
        }
    
    def run_audit(self) -> Dict:
        """Run comprehensive security audit"""
        print("Starting security audit...")
        
        # Check hardcoded secrets
        self.check_hardcoded_secrets()
        
        # Check password security
        self.check_password_security()
        
        # Check input validation
        self.check_input_validation()
        
        # Check configuration security
        self.check_configuration_security()
        
        # Check file permissions
        self.check_file_permissions()
        
        # Check for known vulnerabilities
        self.check_vulnerabilities()
        
        # Generate report
        return self.generate_report()
    
    def check_hardcoded_secrets(self) -> None:
        """Check for hardcoded secrets and keys"""
        print("Checking for hardcoded secrets...")
        
        secret_patterns = [
            r'["\']secret[_\s]?key["\']:\s*["\'][\w\/\+=]{16,}["\']',
            r'["\']password["\']:\s*["\'][\w\/\+=]{8,}["\']',
            r'["\']api[_\s]?key["\']:\s*["\'][\w\/\+=]{16,}["\']',
            r'["\']token["\']:\s*["\'][\w\/\+=]{16,}["\']',
        ]
        
        files_to_check = [
            'app/config.py',
            'app/services/store.py',
            'app/routers/auth.py',
        ]
        
        for file_path in files_to_check:
            full_path = self.project_path / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            self.findings.append({
                                'file': file_path,
                                'line': content[:match.start()].count('\n') + 1,
                                'severity': 'CRITICAL',
                                'type': 'Hardcoded Secret',
                                'description': f'Potential hardcoded secret found: {match.group()}',
                                'recommendation': 'Use environment variables for secrets'
                            })
    
    def check_password_security(self) -> None:
        """Check password security implementation"""
        print("Checking password security...")
        
        store_file = self.project_path / 'app/services/store.py'
        if store_file.exists():
            with open(store_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for weak hashing
                if 'hashlib.sha256' in content:
                    self.findings.append({
                        'file': 'app/services/store.py',
                        'line': content.find('hashlib.sha256') + 1,
                        'severity': 'HIGH',
                        'type': 'Weak Password Hashing',
                        'description': 'Using SHA256 for password hashing is insecure',
                        'recommendation': 'Use bcrypt or Argon2 for password hashing'
                    })
                
                # Check for hardcoded passwords
                if '"omega"' in content:
                    self.findings.append({
                        'file': 'app/services/store.py',
                        'line': content.find('"omega"') + 1,
                        'severity': 'CRITICAL',
                        'type': 'Hardcoded Password',
                        'description': 'Hardcoded password "omega" found in authentication',
                        'recommendation': 'Remove hardcoded passwords and use proper authentication'
                    })
    
    def check_input_validation(self) -> None:
        """Check input validation implementation"""
        print("Checking input validation...")
        
        auth_file = self.project_path / 'app/routers/auth.py'
        if auth_file.exists():
            with open(auth_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for Pydantic models
                if 'BaseModel' not in content:
                    self.findings.append({
                        'file': 'app/routers/auth.py',
                        'line': 1,
                        'severity': 'MEDIUM',
                        'type': 'Missing Input Validation',
                        'description': 'No Pydantic models for input validation',
                        'recommendation': 'Implement Pydantic models for input validation'
                    })
                
                # Check for form validation
                if '@router.post("/login")' in content and 'validate_email' not in content:
                    self.findings.append({
                        'file': 'app/routers/auth.py',
                        'line': content.find('@router.post("/login")') + 1,
                        'severity': 'MEDIUM',
                        'type': 'Missing Email Validation',
                        'description': 'No email format validation in login',
                        'recommendation': 'Add email format validation using Pydantic EmailStr'
                    })
    
    def check_configuration_security(self) -> None:
        """Check configuration security"""
        print("Checking configuration security...")
        
        config_file = self.project_path / 'app/config.py'
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for debug mode in production
                if 'debug: bool = True' in content:
                    self.findings.append({
                        'file': 'app/config.py',
                        'line': content.find('debug: bool = True') + 1,
                        'severity': 'HIGH',
                        'type': 'Debug Mode Enabled',
                        'description': 'Debug mode is hardcoded to True',
                        'recommendation': 'Set debug mode based on environment variable'
                    })
                
                # Check for secret key usage
                if 'change-me-in-production' in content:
                    self.findings.append({
                        'file': 'app/config.py',
                        'line': content.find('change-me-in-production') + 1,
                        'severity': 'CRITICAL',
                        'type': 'Default Secret Key',
                        'description': 'Using default secret key phrase',
                        'recommendation': 'Use environment variable for secret key'
                    })
    
    def check_file_permissions(self) -> None:
        """Check file permissions"""
        print("Checking file permissions...")
        
        # Check for world-readable files
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    stat = os.stat(file_path)
                    if stat.st_mode & 0o044:  # World-readable
                        if file.endswith('.py') or file.endswith('.env'):
                            self.findings.append({
                                'file': str(file_path.relative_to(self.project_path)),
                                'line': 1,
                                'severity': 'MEDIUM',
                                'type': 'World-Readable File',
                                'description': f'File {file_path} is world-readable',
                                'recommendation': 'Restrict file permissions'
                            })
                except OSError:
                    continue
    
    def check_vulnerabilities(self) -> None:
        """Check for common vulnerabilities"""
        print("Checking for vulnerabilities...")
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'execute\s*\([^)]+%\)',
            r'cursor\.execute\s*\([^)]+%\)',
            r'query\s*=\s*[f"\'\"][^"\'\"]*\%',
        ]
        
        files_to_check = ['app/**/*.py']
        
        for pattern in sql_patterns:
            for root, dirs, files in os.walk(self.project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = Path(root) / file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            matches = re.finditer(pattern, content, re.IGNORECASE)
                            for match in matches:
                                self.findings.append({
                                    'file': str(file_path.relative_to(self.project_path)),
                                    'line': content[:match.start()].count('\n') + 1,
                                    'severity': 'CRITICAL',
                                    'type': 'Potential SQL Injection',
                                    'description': 'Potential SQL injection found',
                                    'recommendation': 'Use parameterized queries'
                                })
    
    def generate_report(self) -> Dict:
        """Generate security audit report"""
        print("Generating audit report...")
        
        # Sort findings by severity
        sorted_findings = sorted(
            self.findings,
            key=lambda x: self.severity_levels.get(x['severity'], 0),
            reverse=True
        )
        
        # Count findings by severity
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for finding in sorted_findings:
            severity_counts[finding['severity']] += 1
        
        report = {
            'summary': {
                'total_findings': len(sorted_findings),
                'critical': severity_counts['CRITICAL'],
                'high': severity_counts['HIGH'],
                'medium': severity_counts['MEDIUM'],
                'low': severity_counts['LOW'],
                'risk_level': self.calculate_risk_level(severity_counts)
            },
            'findings': sorted_findings,
            'recommendations': self.generate_recommendations(sorted_findings)
        }
        
        return report
    
    def calculate_risk_level(self, severity_counts: Dict) -> str:
        """Calculate overall risk level"""
        total_score = (
            severity_counts['CRITICAL'] * 4 +
            severity_counts['HIGH'] * 3 +
            severity_counts['MEDIUM'] * 2 +
            severity_counts['LOW'] * 1
        )
        
        if total_score >= 20:
            return "CRITICAL"
        elif total_score >= 10:
            return "HIGH"
        elif total_score >= 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_recommendations(self, findings: List) -> List:
        """Generate security recommendations"""
        recommendations = []
        
        if any(f['severity'] == 'CRITICAL' for f in findings):
            recommendations.append({
                'priority': 'IMMEDIATE',
                'action': 'Address all CRITICAL vulnerabilities immediately',
                'description': 'Critical vulnerabilities can lead to complete system compromise'
            })
        
        if any('Hardcoded Secret' in f['type'] for f in findings):
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Implement environment variable management',
                'description': 'Use environment variables for all secrets and keys'
            })
        
        if any('Password' in f['type'] for f in findings):
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Implement secure password hashing',
                'description': 'Use bcrypt or Argon2 for password hashing'
            })
        
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'Implement input validation',
            'description': 'Add Pydantic models for all user inputs'
        })
        
        return recommendations

def main():
    """Main function"""
    project_path = "C:\\Users\\USER\\belentani-the-judas-experience"
    
    auditor = SecurityAuditor(project_path)
    report = auditor.run_audit()
    
    # Print summary
    print("\n" + "="*50)
    print("SECURITY AUDIT SUMMARY")
    print("="*50)
    print(f"Total Findings: {report['summary']['total_findings']}")
    print(f"Critical: {report['summary']['critical']}")
    print(f"High: {report['summary']['high']}")
    print(f"Medium: {report['summary']['medium']}")
    print(f"Low: {report['summary']['low']}")
    print(f"Risk Level: {report['summary']['risk_level']}")
    
    # Print recommendations
    print("\nRECOMMENDATIONS:")
    print("-"*50)
    for rec in report['recommendations']:
        print(f"[{rec['priority']}] {rec['action']}")
        print(f"  {rec['description']}")
        print()
    
    # Save report
    report_path = Path(project_path) / "security_audit_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Audit report saved to: {report_path}")
    
    return report

if __name__ == "__main__":
    main()