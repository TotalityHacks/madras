'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant_groups', {
  }, {
    tableName: 'registration_applicant_groups',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'applicant_id',
      
      as: '_applicant_id',
    });
    
    Model.belongsTo(models.auth_group, {
      foreignKey: 'group_id',
      
      as: '_group_id',
    });
    
  };

  return Model;
};

