# CLI Wizard Migration Guide

## Overview

This guide provides instructions for migrating from the legacy CLI wizard system to the new modular architecture.

## Migration Timeline

### Phase 1: Coexistence Period (2 weeks)
- Both old and new systems operate simultaneously
- Users can choose which system to use
- New system gradually becomes default

### Phase 2: Transition Period (2 weeks)  
- New system becomes default
- Legacy system available via explicit opt-in
- User education and training

### Phase 3: Deprecation (1 week)
- Legacy system officially deprecated
- Removal scheduled for next major release

## Coexistence Strategy

### Running Both Systems

During the coexistence period, both systems will be available:

**New System** (via new command):
```bash
media-knowledge-launch-v2
```

**Legacy System** (current command):
```bash
media-knowledge-launch
```

### Gradual Migration

Users will be prompted to try the new system:

```
New enhanced wizard system available!
Type 'launch-v2' to try the improved experience
```

## Technical Migration Details

### Backend Compatibility

The new wizard system maintains complete CLI command compatibility:

| Legacy Command | New Equivalent | Notes |
|----------------|----------------|-------|
| `media-knowledge process media` | Same | Unchanged |
| `media-knowledge batch process-urls` | Same | Unchanged |  
| `media-knowledge document process` | Same | Unchanged |
| `media-knowledge anki generate` | Same | Unchanged |

### Configuration Preservation

User preferences and settings will be automatically migrated:

```python
# Migration script will handle:
# - Template preferences
# - Default output directories  
# - Processing options history
# - Bookmark locations
```

## User Experience Changes

### Improvements in New System

1. **Consistent Interface**: All workflows now have unified UX
2. **Better Validation**: More robust input checking
3. **Enhanced Help**: Context-sensitive assistance at each step
4. **Clearer Errors**: More informative error messages
5. **Faster Navigation**: Streamlined workflow progression

### What Stays the Same

- All existing functionality preserved
- Same CLI command equivalents
- Identical output file locations
- Compatible with existing automation scripts

## Developer Migration

### Code Structure Changes

**Legacy Structure:**
```
src/media_knowledge/cli/frontend/
├── media_wizard.py
├── batch_wizard.py  
├── document_wizard.py
└── anki_wizard.py
```

**New Structure:**
```
src/media_knowledge/cli/frontend/
├── main_menu.py
├── shared/
│   ├── input_validator.py
│   └── user_prompter.py
└── workflows/
    ├── base_workflow.py
    ├── media_workflow.py
    ├── batch_workflow.py
    ├── document_workflow.py
    └── anki_workflow.py
```

### API Changes

Most APIs remain backward compatible. Breaking changes:

1. **Wizard Classes**: Removed individual wizard classes
2. **State Management**: New centralized system
3. **Error Handling**: Updated exception hierarchy

### Testing Migration

Existing tests should continue to pass with minimal changes. Update imports if testing specific wizard classes:

```python
# Old import
from src.media_knowledge.cli.frontend.media_wizard import MediaWizard

# New import  
from src.media_knowledge.cli.frontend.workflows.media_workflow import MediaWorkflow
```

## Rollback Procedure

If issues arise during migration:

### Immediate Rollback

1. Switch users back to legacy system
2. Disable new system access
3. Apply emergency patches to legacy system

### Selective Rollback

1. Identify problematic workflows
2. Revert specific components  
3. Monitor system stability

## Monitoring and Support

### Migration Metrics

Track these key metrics during migration:

- User adoption rate of new system
- Error rates comparison between systems
- Performance benchmarks
- User satisfaction scores

### Support Resources

Provide users with:

- Migration FAQ document
- Side-by-side comparison guide
- Live support during transition
- Feedback collection channel

## FAQ for Users

### Will my existing scripts break?
No. All CLI commands remain identical and fully compatible.

### Do I need to reconfigure my preferences?
No. Your settings will be automatically migrated.

### Can I switch back if I don't like the new system?
Yes. During the transition period, you can choose either system.

### What if I encounter issues?
Contact support immediately. Both systems will be available during troubleshooting.

## FAQ for Developers

### How much code needs to change?
Minimal changes required for most integrations. Primary changes involve:
- Updated import paths
- New workflow instantiation methods
- Updated error handling patterns

### What about custom extensions?
Custom extensions will need to be adapted to the new architecture, but the migration guide provides clear patterns.

### When will legacy code be removed?
Legacy code will be officially deprecated 30 days after new system launch, with removal targeted for next major version.

### Are there training resources?
Yes, comprehensive developer documentation and migration workshops will be provided.

## Feedback Process

Collect user and developer feedback through:

1. **Surveys**: Regular feedback collection
2. **Usage Analytics**: Track adoption and performance
3. **Support Tickets**: Monitor issue patterns
4. **Community Forums**: Open discussion channels

## Success Criteria

Migration considered successful when:

- 95%+ user adoption of new system
- Zero critical bugs reported
- Performance metrics meet or exceed baseline
- User satisfaction scores remain high
- No data loss incidents

## Emergency Procedures

### Critical Bug Response

1. **Immediate**: Issue mitigation workaround
2. **Short-term**: Hotfix deployment  
3. **Long-term**: Root cause analysis and permanent fix

### Data Loss Prevention

Daily backups of user configurations and preferences during transition period.

## Communication Plan

### Internal Stakeholders
- Weekly migration status updates
- Daily standups during transition period
- Real-time incident communication

### External Users
- Email notifications for major milestones
- In-app announcements for feature changes
- Updated documentation for new features

## Training and Education

### User Training
- Interactive tutorial for new interface
- Video walkthroughs of key workflows  
- Quick reference guides
- Live Q&A sessions

### Developer Training  
- Technical workshops on new architecture
- Code review sessions
- Pair programming for complex integrations
- Updated API documentation

This comprehensive migration guide ensures smooth transition from legacy to modern CLI wizard system while maintaining system reliability and user satisfaction.