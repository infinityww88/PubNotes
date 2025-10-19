# Validator

Tools/Odin Project Validator，使用一个选择的 profile 运行一个 scan，并将扫描的结果呈现给你。因此你可以遍历所有 validation 结果，进行必要的修复。

## Validating ScriptableObjects and Components

Odin validator 包含内置的对以下 validation attributes 的支持

- RequireComponent（必需组件）
- AssetsOnly（仅资源）
- FilePath, when RequireExistingPath is set to true
- FolderPath, when RequireExisting Path is set to true
- ChildGameObjectsOnly（仅子物体）
- SceneObjectsOnly（仅 scene 中的物体）
- DetailedInfoBox when an error is shown（出现错误时显示 DetailedInfoBox）
- InfoBox when an error is shown
- Required
- ValidateInput
- MinValue
- MaxValue
- Range and PropertyRange
- MinMaxSlider

When used diligently throughout your project, Odin Project Validator makes it easier to onboard new team members, and helps keeps your project stable as it grows and changes.

## Creating custom validators

- Add your own validation attributes
- Create general project-wide validation rules that apply regardless of attributes
- check all saved strings in the entire project
  - [assembly: RegisterValidator(typeof(EmptyStringValidator))]
  - public class EmptyStringValidator : ValueValidator\<string>
  - protected override void Validate(string value, ValidationResult result)
  - result.ResultType = ValidationResultType.Warning;
  - result.Message = "This string is empty! Are you sure that's correct?";
- check any string value with [Regex] applied
  - [assembly: RegisterValidator(typeof(RegeValidator))]
  - public class RegexAttribute : Attribute {}
  - public class RegexValidator : AttributeValidator<RegexAttribute, string>
  - protected override void Validate(object parentInstance, string memberValue, MemberInfo member, ValidationResult result)
  - result.ResultType = VailidationResultType.Error;
  - result.Message = "Invalid regex string: " + ex.Message;

## Odin Validation Profiles

- Each validation profile is a scriptable object, stored in Sirenix/Odin Validator/Editor/Config/.
- All of these profiles can be modified, renamed, removed and reset to suit your needs.
- Validation Profiles defines the scope or source for a validation scan.
- deault validation profiles
  - Scan entire project: Scans all prefabs, scriptable objects and scenes your project.
  - Scan all assets: Scans all prefabs and scriptable objects in your project.
  - Scan all scenes: Scans all scenes in your project, without going through scene asset dependencies.
  - Scan Open Scens: Scans all open scens, without going through scene asset dependencies.
  - Scan scenes from build options: Scans all scenes from build options, including scene asset dependencies.
- Built-in Validation Profiles
  - All of the default validation profiles are made up of 3 diferent types of validation profiles
    - Asset Validation Profile
      - Search Filters: specify which types of assets should be scanned, such as t:ScriptableObject, t:Prefab, and t:Material
      - AssetPaths: specify which paths should be included. All assets that match the filter will be included. You can also specify individual file paths
      - AssetReferences: drag to specify an individual asset references to scan so you don't have to worry about where they are located
      - ExcludeAssetPath: specify entire folders or individual files which should be excluded
      - ExcludeAssetReferences: specify individual asset references which should be excluded
    - Scene Validation Profile
      - Scene Paths: specify a folder path will include all scenes located within that folder. You can also specify paths to individual scenes.
      - Exclude Scene Paths: like Scene Paths, but exclude those scenes
      - Include Scenes From Build Options: includes all active scenes listed in the current build options
      - Include Open Scenes: scan all currently open scenes
      - Include Asset Dependencies: Enabling this will locate the asset dependencies of all scanned scenes and validate those as well.
    - Collection Validation Profile
      - Let you combine multiple validation profiles together in a single profile
      - Profiles: A list of Validation profiles to run

## Custom Validation Profile

- Odin Project Validator comes with three different validation profile types: AssetValidationProfile, SceneValidationProfile and CollectionValidationProfile. These profile types cover most use-cases.
- Implement IValidationProfile interface.
- Should be a regular C# type, not a Unity object, and store custom validation profile instance in a host scriptable object asset, so it can be easily configured and added to the Validation Profile Manager.
  - [CreateAssetMenu] public class MyDatabaseValidatorAsset : ValidationProfileAsset\<MyDatabaseValidator> {}
  - [Serializable] public class MyDatabaseValidator: IValidationProfile
  - public IEnumerable\<ValidationProfileResult> Validate(ValidationRunner runner)
  - runner.ValidateValue(item, null, ref results.Results);
  - Calling ValidateValue will use all defined Validators, and populate the results with errors and warnings.

## Running a Validation Profile from code

- First get or create the validation profile
  - instantiate validation profiles and configure them manually
  - load them from the asset database
- ValidationProfileManagerWindow.OpenProjectValidatorWithProfile(profileToRun, scanProfileImmediately: true);
- manually run a validation profile
  - ValidationRunner runner = new ValidationRunner();
  - foreach (ValidationProfileResult vpResult in profileToRun.Validate(runner))
    - foeach (ValidationResult result in vpResult.Results)
