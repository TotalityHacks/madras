'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant_user_permissions', {
  }, {
    tableName: 'registration_applicant_user_permissions',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'applicant_id',
      
      as: '_applicant_id',
    });
    
    Model.belongsTo(models.auth_permission, {
      foreignKey: 'permission_id',
      
      as: '_permission_id',
    });
    
  };

  return Model;
};

